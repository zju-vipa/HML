function res = generate_datas_function(data_path, list_load,list_line,list_linef,list_time)
%GENERATE_DATAS_FUNCTION 此处显示有关此函数的摘要
%   此处显示详细说明
% clear;clc
% addpath(genpath('matpower7.1'));
% addpath(genpath('psat'));
res = 1;
initpsat;%初始化PSAT
RESULT.all = [];
% list_load = [0.8, 0.85, 0.9, 0,95, 1.0, 1.05, 1.1, 1.15, 1.2];
% list_line = [1:34];
% list_linef = [0.2, 0.4, 0.6, 0.8];
% list_time = [1.0/60, 2.0/60, 4.0/60, 8.0/60];


data.label = [];
data.bus_matrix = [];
data.gen_matrix = [];
for fault_line = list_line  %遍历故障线路
    %data.label = [];
    %data.bus_matrix = [];
    %data.gen_matrix = [];
for fault_percentage = list_linef    %遍历线路故障位置
for random_load = list_load  %遍历负荷调整   
for fault_time = list_time  %遍历故障持续时间
%for fault_line = list_line  %遍历故障线路
%for fault_percentage = list_linef    %遍历线路故障位置
%for random_load = list_load
%for fault_time = list_time
%% 发生三相短路故障的线路号，数据在文件Init_data中的mpc.line中
%  1-34号为正常线路，35-46号为带有变压器的线路

% fault_line=floor(34.*rand(1,1)+1);   %1-34随机故障
%% 故障持续的时间，大于0，单位是秒，一般取0-0.3之间
%fault_time=rand(1,1)./8;     %随机故障持续时间   randperm(11,1)./60
% fault_time=randperm(11,1)./60; %可选故障持续时间
%% 故障之后是否切除发生故障的那条线路，1表示切除短路故障的线路，0表示不切除故障线路故障自动消除
fault_whether_cutline=1;
%% 故障在该条线路上的具体地点，以百分比展示
%  0表示发生在mpc.line中的from一端，1表示在to那一端，0.5表示线路中点，用[0,1]之间的数进行表示
%fault_percentage=double(rand(1)>=0.5);%(randperm(10,1)-1)./10
% fault_percentage=double((randperm(10,1)-1)./10); %可选故障地点 线路0~90%，步长为10%
%% 随机负荷，随机发电机出力的仿真进行的次数,1额定负荷。2随机负荷
%fault_random=double(rand(1)>=0.1)+1;
fault_random = 2;

%% 判断输入数据是否符合要求
if fix(fault_line)~=fault_line
    warning('发生故障的线路号fault_line必须为整数');
    continue;
end
if (fault_line<=0)||(fault_line>46)
    warning('发生故障的线路号fault_line越界，请输入1-46');
    continue;
end
if (fault_line>=35)&&(fault_line<=46)&&(fault_percentage~=0)&&(fault_percentage~=1)
    warning('带有变压器的线路只能在首末两端设置发生故障');
    continue;
end

%% 对输入数据进行处理
Init_datanew; %导入原始数据，存在mpc结构体中
 
%% 对故障发生时间相关数据进行处理
mpc.fault(:,6)=fault_time+mpc.fault(:,5);  %mpc.fault(:,5)故障发生时间，mpc.fault(:,6)故障切除时间


%% 对随机负荷进行处理
abc=loadcase('case39');
if fault_random==1
    opf_result=opf(abc);
else
    %让负荷在基础负荷10%的范围内波动
%     random_load=0.9+0.2.*rand(39,1);
    abc.bus(:,3)=abc.bus(:,3).*random_load;
    abc.bus(:,4)=abc.bus(:,4).*random_load;
    %发电机出力在40%范围内波动
    abc.gen(:,9)=1.4.*abc.gen(:,2);%Pmax
    abc.gen(:,10)=0.6.*abc.gen(:,2);%Pmin
    %计算新随机情形下的opf，得到新情形下的潮流数据
    opf_result=opf(abc);
    %平衡节点的V、Theta的处理
    mpc.SW(:,4)=opf_result.bus(31,8);
    mpc.SW(:,5)=opf_result.bus(31,9);
    %PV节点的处理
    mpc.PV(:,4)=([opf_result.gen(1,2);opf_result.gen(3:10,2)]-[opf_result.bus(30,3);opf_result.bus(32:39,3)])./100;
    mpc.PV(:,5)=[opf_result.gen(1,6);opf_result.gen(3:10,6)];
    %PQ节点的处理
    mpc.PQ(:,4)=opf_result.bus(1:29,3)./100;
    mpc.PQ(:,5)=opf_result.bus(1:29,4)./100;
end

%% 对故障地点、断路器地点及其切除时间进行处理
if fault_percentage==0
    fault_bus=mpc.line(fault_line,1);%线路首端节点故障
    mpc.fault(:,1)=fault_bus;
    mpc.breaker(1,1)=fault_line;%故障要切除的线路号
    mpc.breaker(1,2)=fault_bus;%故障要切除的线路在哪个节点旁装断路器
    mpc.breaker(1,7)=mpc.fault(1,6);%线路切除的时间
    mpc.breaker(1,9)=fault_whether_cutline;%是否要切除线路
else if fault_percentage==1
        fault_bus=mpc.line(fault_line,2);%线路末端节点故障
        mpc.fault(:,1)=fault_bus;
        mpc.breaker(1,1)=fault_line;%故障要切除的线路号
        mpc.breaker(1,2)=fault_bus;%故障要切除的线路在哪个节点旁装断路器
        mpc.breaker(1,7)=mpc.fault(1,6);%线路切除的时间
        mpc.breaker(1,9)=fault_whether_cutline;%是否要切除线路
    else
        fault_bus=40;%在线路中间新弄一个节点，当不是10机39节点系统时，此处需要%%%修改%%%
        mpc.fault(:,1)=fault_bus;
        %对参数进行修改，使其有40个节点，并且对rxb进行修改
        mpc.bus=[mpc.bus;40,100,1,0,1,1];
        mpc.PQ=[mpc.PQ;40,100,100,0,0,1.2,0.8,0,1];
        mpc.line=[mpc.line;mpc.line(fault_line,:)];   %实际上不存在的新线路
        
        mpc.line(fault_line,2)=40;    %把故障线路的末端节点改为新节点(40)
        mpc.line(fault_line,8)=mpc.line(fault_line,8).*fault_percentage;   %相当于改变r x b
        mpc.line(fault_line,9)=mpc.line(fault_line,9).*fault_percentage;
        mpc.line(fault_line,10)=mpc.line(fault_line,10).*fault_percentage;
        
        mpc.line(size(mpc.line,1),1)=40;   %%把新线路的首端节点改为新节点(40)
        mpc.line(size(mpc.line,1),8)=mpc.line(size(mpc.line,1),8).*(1-fault_percentage);
        mpc.line(size(mpc.line,1),9)=mpc.line(size(mpc.line,1),9).*(1-fault_percentage);
        mpc.line(size(mpc.line,1),10)=mpc.line(size(mpc.line,1),10).*(1-fault_percentage);
        
        mpc.breaker=[mpc.breaker;mpc.breaker];
        mpc.breaker(1,1)=fault_line;%故障要切除的线路号
        mpc.breaker(2,1)=size(mpc.line,1);
        mpc.breaker(1,2)=mpc.line(fault_line,1);%故障要切除的线路在哪个节点旁装断路器
        mpc.breaker(2,2)=mpc.line(size(mpc.line,1),2);
        mpc.breaker(1,7)=mpc.fault(1,6);%线路切除的时间
        mpc.breaker(2,7)=mpc.fault(1,6);
        mpc.breaker(1,9)=fault_whether_cutline;%是否要切除线路
        mpc.breaker(2,9)=fault_whether_cutline;
    end
end

%将数据转化为psat认可的m文件
mat2m; %转换文件格式
runpsat('d_039_ieee','data');
Settings.t0=0;
Settings.tf=10; %5
Settings.fixt=1;%是否固定步长
Settings.tstep=0.01;
Settings.freq=60;

Varname.idx = [1:125+4*size(mpc.bus,1)+4*size(mpc.line,1)];

clpsat.mesg=1;  
Varname.P=1;
Varname.Q=1;

%NN=(Settings.tf-Settings.t0)./Settings.tstep+1;
runpsat('td');  %TDS 

%读出数据模型阶数
gen_model=mpc.syn(:,[1,5]);
gen_model=sortrows(gen_model,1);
gen_model_sum=0;
%记录下theta和omega的值
RESULTS.theta=[];
RESULTS.omega=[];
RESULTS.pm=[];
RESULTS.e_p=[];
RESULTS.t=Varout.t;
RESULTS.bus_u=[];
RESULTS.bus_theta=[];
RESULTS.bus_p = [];
RESULTS.bus_q = [];
%% Varout中，203列变量含义为：40(发电机四阶模型状态变量)+4*9=36(励磁调速状态变量)+39(母线电压相角)+39(母线电压幅值)+？？？(不知道是什么)
for i=1:size(mpc.syn,1)
    RESULTS.theta=[RESULTS.theta;Varout.vars(:,gen_model_sum+1)'];   %列为变量(t) 状态变量···记录发电机theta
    RESULTS.omega=[RESULTS.omega;Varout.vars(:,gen_model_sum+2)'];   %记录发电机omega
%     RESULTS.pm=[RESULTS.pm;Varout.vars(:,186+4*i)'];
    gen_model_sum=gen_model_sum+gen_model(i,2);
%     RESULTS.e_p=[RESULTS.e_p;sqrt((Varout.vars(:,178+i)+Varout.vars(:,188+4.*i).*mpc.syn(i,9)./Varout.vars(:,178+i)).^2+(Varout.vars(:,187+4.*i).*mpc.syn(i,9)./Varout.vars(:,178+i)).^2)'];
end
RESULTS.whole=Varout.vars;

for i = 1:size(mpc.bus,1)
    RESULTS.bus_theta = [RESULTS.bus_theta;Varout.vars(:,DAE.n+i)'];        %记录母线电压相角
    RESULTS.bus_u = [RESULTS.bus_u;Varout.vars(:,DAE.n+Bus.n+i)'];          %记录母线电压幅值
    RESULTS.bus_p = [RESULTS.bus_p;Varout.vars(:,DAE.n+DAE.m+i)'];          %记录母线有功功率
    RESULTS.bus_q = [RESULTS.bus_q;Varout.vars(:,DAE.n+DAE.m+Bus.n+i)'];    %记录母线无功功率
end
    
% for i = 1:size(mpc.syn,1)
%     RESULTS.gen_thets = 
% end

RESULTS.fault_line=fault_line;
RESULTS.fault_time=fault_time;
RESULTS.fault_percentage=fault_percentage;
RESULTS.fault_whether_cutline=fault_whether_cutline;
RESULTS.fault_random=fault_random;
RESULTS.line = mpc.line;
[~,t] = size(RESULTS.bus_u);

if t >1000
    ts_time = mpc.fault(:,6);  % trouble shoot time 
    [indx,~]=find(Varout.t>ts_time);
    % bus
    ts_bus_u = RESULTS.bus_u(:,indx(1));
    ts_bus_t = RESULTS.bus_theta(:,indx(1));
    ts_bus_p = RESULTS.bus_p(:,indx(1));
    ts_bus_q = RESULTS.bus_q(:,indx(1));
    bus_vecs = [ts_bus_u,ts_bus_t,ts_bus_p,ts_bus_q];
    % gen
    ts_gen_v1 = RESULTS.whole(indx(1),1:4:40);
    ts_gen_v2 = RESULTS.whole(indx(1),2:4:40);
    ts_gen_v3 = RESULTS.whole(indx(1),3:4:40);
    ts_gen_v4 = RESULTS.whole(indx(1),4:4:40);
    gen_vecs = [ts_gen_v1, ts_gen_v2, ts_gen_v3, ts_gen_v4];
    %load？
    %ts_load = 
    %label
    gen_theta = RESULTS.theta(:,t);
    max_theta = max(gen_theta);
    min_theta = min(gen_theta);
    if max_theta - min_theta < 360
       label = 1; 
    else
       label = 0; 
    end
    data.label = [data.label;label];
    data.line = mpc.line;
    data.bus_matrix = cat(3,data.bus_matrix, bus_vecs);
    data.gen_matrix = cat(3,data.gen_matrix, gen_vecs);
    %data_path = ['data','\',num2str(label),'_',num2str(fault_line),'_',num2str(fault_percentage),'_',num2str(fault_time),'_',num2str(random_load),'.mat'];
    %if exist(data_path,'file')
    %    continue; 
    %else 
    %save(data_path,'data');
    %end
end
    disp(['fault_line:',num2str(fault_line), ' fault_percentage:',num2str(fault_percentage),' load:',num2str(random_load),' fault_time:',num2str(fault_time)])
end
end
end
    %data_path = ['data1','\','m10case39','_line', num2str(fault_line),'.mat'];
end
    save(data_path,'data');
    res = 2;
end

