import os
import torch
import torch.nn as nn
import torch.nn.functional as torch_fn

os.environ["DGLBACKEND"] = 'pytorch'
import dgl
import dgl.function as fn


class FactorGNN(nn.Module):
    def __init__(self,
                 g,
                 in_dim,
                 num_hidden,
                 num_classes,
                 num_latent,
                 feat_drop,
                 ):
        super(FactorGNN, self).__init__()
        self.g = g
        self.layers = nn.ModuleList()
        self.BNs = nn.ModuleList()
        self.linears = nn.ModuleList()
        self.feat_drop = feat_drop

        self.linears.append(nn.Linear(in_dim, num_classes))

        self.layers.append(DisentangleLayer(num_latent, in_dim, num_hidden, cat=True))
        self.BNs.append(nn.BatchNorm1d(num_hidden))
        self.linears.append(nn.Linear(num_hidden, num_classes))

        self.layers.append(DisentangleLayer(num_latent, num_hidden, num_hidden, cat=True))
        self.BNs.append(nn.BatchNorm1d(num_hidden))
        self.linears.append(nn.Linear(num_hidden, num_classes))

        self.layers.append(DisentangleLayer(max(num_latent // 2, 1), num_hidden, num_hidden, cat=True))
        self.BNs.append(nn.BatchNorm1d(num_hidden))
        self.linears.append(nn.Linear(num_hidden, num_classes))

        self.layers.append(DisentangleLayer(max(num_latent // 2, 1), num_hidden, num_hidden, cat=True))
        self.BNs.append(nn.BatchNorm1d(num_hidden))
        self.linears.append(nn.Linear(num_hidden, num_classes))

        self.layers.append(DisentangleLayer(max(num_latent // 2 // 2, 1), num_hidden, num_hidden, cat=True))
        self.BNs.append(nn.BatchNorm1d(num_hidden))
        self.linears.append(nn.Linear(num_hidden, num_classes))

        self.activate = torch.nn.ReLU()

    def forward(self, inputs):
        self.feat_list = []

        feat = inputs
        self.feat_list.append(feat)
        for layer, bn in zip(self.layers, self.BNs):
            # feat = torch_fn.dropout(feat, self.feat_drop)
            pre_feat = feat
            feat = layer(self.g, feat)
            feat = bn(feat)
            # feat = feat + pre_feat
            feat = self.activate(feat)

            self.feat_list.append(feat)

        logit = 0
        for feat, linear in zip(self.feat_list, self.linears):
            self.g.ndata['h'] = feat
            # h = dgl.sum_nodes(self.g, 'h')
            h = self.g.ndata['h']
            # h = self.activate(h)
            h = linear(h)
            logit += torch_fn.dropout(h, self.feat_drop)

        return logit

    def get_hidden_feature(self):
        return self.feat_list

    def get_factor(self):
        # return factor graph at each disentangle layer as list
        factor_list = []
        for layer in self.layers:
            if isinstance(layer, DisentangleLayer):
                factor_list.append(layer.get_factor())
        return factor_list

    def compute_disentangle_loss(self):
        # compute disentangle loss at each layer
        # return: list of loss
        loss_list = []
        for layer in self.layers:
            if isinstance(layer, DisentangleLayer):
                loss_list.append(layer.compute_disentangle_loss())
        return loss_list

    @staticmethod
    def merge_loss(list_loss):
        total_loss = 0
        for loss in list_loss:
            discrimination_loss = loss
            total_loss += discrimination_loss
        return total_loss


class DisentangleLayer(nn.Module):
    def __init__(self, n_latent, in_dim, out_dim, cat=True):
        super(DisentangleLayer, self).__init__()
        # init self.g as None, after forward step, it will be replaced
        self.g = None

        self.n_latent = n_latent
        self.n_feat_latent = out_dim // self.n_latent if cat else out_dim
        self.cat = cat

        self.linear = nn.Linear(in_dim, self.n_feat_latent)
        self.att_ls = nn.ModuleList()
        self.att_rs = nn.ModuleList()
        for latent_i in range(self.n_latent):
            self.att_ls.append(nn.Linear(self.n_feat_latent, 1))
            self.att_rs.append(nn.Linear(self.n_feat_latent, 1))

        # define for the additional losses
        self.graph_to_feat = GraphEncoder(self.n_feat_latent, self.n_feat_latent // 2)
        self.classifier = nn.Linear(self.n_feat_latent, self.n_latent)
        self.loss_fn = nn.CrossEntropyLoss()

    def forward(self, g, inputs):
        self.g = g.local_var()
        out_feats = []
        hidden = self.linear(inputs)
        self.hidden = hidden
        for latent_i in range(self.n_latent):
            # compute factor features of nodes
            a_l = self.att_ls[latent_i](hidden)
            a_r = self.att_rs[latent_i](hidden)
            self.g.ndata.update({f'feat_{latent_i}': hidden,
                                 f'a_l_{latent_i}': a_l,
                                 f'a_r_{latent_i}': a_r})
            self.g.apply_edges(fn.u_add_v(f'a_l_{latent_i}', f'a_r_{latent_i}', f"factor_{latent_i}"))
            self.g.edata[f"factor_{latent_i}"] = torch.sigmoid(6.0 * self.g.edata[f"factor_{latent_i}"])
            feat = self.g.ndata[f'feat_{latent_i}']

            # graph conv on the factor graph
            norm = torch.pow(self.g.in_degrees().float().clamp(min=1), -0.5)
            shp = norm.shape + (1,) * (feat.dim() - 1)
            norm = torch.reshape(norm, shp).to(feat.device)
            feat = feat * norm

            # generate the output features
            self.g.ndata['h'] = feat
            self.g.update_all(fn.u_mul_e('h', f"factor_{latent_i}", 'm'),
                              fn.sum(msg='m', out='h'))
            out_feats.append(self.g.ndata['h'].unsqueeze(-1))

        if self.cat:
            return torch.cat(tuple([rst.squeeze(-1) for rst in out_feats]), -1)
        else:
            return torch.mean(torch.cat(tuple(out_feats), -1), -1)

    def compute_disentangle_loss(self):
        assert self.g is not None, "compute disentangle loss need to be called after forward pass"

        # compute discrimination loss
        factors_feat = [self.graph_to_feat(self.g, self.hidden, f"factor_{latent_i}").squeeze()
                        for latent_i in range(self.n_latent)]

        labels = [torch.ones(f.shape[0]) * i for i, f in enumerate(factors_feat)]
        # labels = torch.cat(tuple(labels), 0).long().cuda()
        labels = torch.cat(tuple(labels), 0).long().to(self.g.device)

        factors_feat = torch.cat(tuple(factors_feat), 0)

        pred = self.classifier(factors_feat)
        discrimination_loss = self.loss_fn(pred, labels)

        return discrimination_loss

    def get_factor(self):
        g = self.g.local_var()
        return g


class GraphEncoder(nn.Module):
    def __init__(self, in_dim, hidden_dim):
        super(GraphEncoder, self).__init__()
        self.linear1 = nn.Linear(in_dim, hidden_dim)
        self.linear2 = nn.Linear(hidden_dim, in_dim)

    def forward(self, g, inputs, factor_key):
        g = g.local_var()
        # graph conv on the factor graph
        feat = self.linear1(inputs)
        norm = torch.pow(g.in_degrees().float().clamp(min=1), -0.5)
        shp = norm.shape + (1,) * (feat.dim() - 1)
        norm = torch.reshape(norm, shp).to(feat.device)
        feat = feat * norm

        g.ndata['h'] = feat
        g.update_all(fn.u_mul_e('h', factor_key, 'm'),
                     fn.sum(msg='m', out='h'))
        g.ndata['h'] = torch.tanh(g.ndata['h'])

        # graph conv on the factor graph
        feat = self.linear2(g.ndata['h'])
        feat = feat * norm

        g.ndata['h'] = feat
        g.update_all(fn.u_mul_e('h', factor_key, 'm'),
                     fn.sum(msg='m', out='h'))
        g.ndata['h'] = torch.tanh(g.ndata['h'])

        h = dgl.mean_nodes(g, 'h').unsqueeze(-1)
        h = torch.tanh(h)

        return h