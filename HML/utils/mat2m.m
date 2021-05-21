%function mat2m=mat2m(mpc)
fid_temp=['d_039_ieee.m'];
fid=fopen(fid_temp,'w+');

%Bus.con
fprintf(fid,'%s\n','Bus.con = [...');
for i=1:size(mpc.bus,1)  %行数
    for j=1:size(mpc.bus,2)
        if mpc.bus(i,j)==fix(mpc.bus(i,j))
            fprintf(fid,'\t%d',mpc.bus(i,j));
        else
            fprintf(fid,'\t%f',mpc.bus(i,j));
        end
        if j==size(mpc.bus,2)
            fprintf(fid,'%s\n',';');
        end
    end
end
fprintf(fid,'%s\n','];');
    
%Line.con
fprintf(fid,'%s\n','Line.con = [...');
for i=1:size(mpc.line,1)  %行数
    for j=1:size(mpc.line,2)
        if mpc.line(i,j)==fix(mpc.line(i,j))
            fprintf(fid,'\t%d',mpc.line(i,j));
        else
            fprintf(fid,'\t%f',mpc.line(i,j));
        end
        if j==size(mpc.line,2)
            fprintf(fid,'%s\n',';');
        end
    end
end
fprintf(fid,'%s\n','];');    

%Breaker.con
fprintf(fid,'%s\n','Breaker.con = [...');
for i=1:size(mpc.breaker,1)  %行数
    for j=1:size(mpc.breaker,2)
        if mpc.breaker(i,j)==fix(mpc.breaker(i,j))
            fprintf(fid,'\t%d',mpc.breaker(i,j));
        else
            fprintf(fid,'\t%f',mpc.breaker(i,j));
        end
        if j==size(mpc.breaker,2)
            fprintf(fid,'%s\n',';');
        end
    end
end
fprintf(fid,'%s\n','];');    

%Fault.con
fprintf(fid,'%s\n','Fault.con = [...');
for i=1:size(mpc.fault,1)  %行数
    for j=1:size(mpc.fault,2)
        if mpc.fault(i,j)==fix(mpc.fault(i,j))
            fprintf(fid,'\t%d',mpc.fault(i,j));
        else
            fprintf(fid,'\t%f',mpc.fault(i,j));
        end
        if j==size(mpc.fault,2)
            fprintf(fid,'%s\n',';');
        end
    end
end
fprintf(fid,'%s\n','];');   

%SW.con
fprintf(fid,'%s\n','SW.con = [...');
for i=1:size(mpc.SW,1)  %行数
    for j=1:size(mpc.SW,2)
        if mpc.SW(i,j)==fix(mpc.SW(i,j))
            fprintf(fid,'\t%d',mpc.SW(i,j));
        else
            fprintf(fid,'\t%f',mpc.SW(i,j));
        end
        if j==size(mpc.SW,2)
            fprintf(fid,'%s\n',';');
        end
    end
end
fprintf(fid,'%s\n','];');   

%PV.con
fprintf(fid,'%s\n','PV.con = [...');
for i=1:size(mpc.PV,1)  %行数
    for j=1:size(mpc.PV,2)
        if mpc.PV(i,j)==fix(mpc.PV(i,j))
            fprintf(fid,'\t%d',mpc.PV(i,j));
        else
            fprintf(fid,'\t%f',mpc.PV(i,j));
        end
        if j==size(mpc.PV,2)
            fprintf(fid,'%s\n',';');
        end
    end
end
fprintf(fid,'%s\n','];');  

%PQ.con
fprintf(fid,'%s\n','PQ.con = [...');
for i=1:size(mpc.PQ,1)  %行数
    for j=1:size(mpc.PQ,2)
        if mpc.PQ(i,j)==fix(mpc.PQ(i,j))
            fprintf(fid,'\t%d',mpc.PQ(i,j));
        else
            fprintf(fid,'\t%f',mpc.PQ(i,j));
        end
        if j==size(mpc.PQ,2)
            fprintf(fid,'%s\n',';');
        end
    end
end
fprintf(fid,'%s\n','];');  

%Syn.con
fprintf(fid,'%s\n','Syn.con = [...');
for i=1:size(mpc.syn,1)  %行数
    for j=1:size(mpc.syn,2)
        if mpc.syn(i,j)==fix(mpc.syn(i,j))
            fprintf(fid,'\t%d',mpc.syn(i,j));
        else
            fprintf(fid,'\t%f',mpc.syn(i,j));
        end
        if j==size(mpc.syn,2)
            fprintf(fid,'%s\n',';');
        end
    end
end
fprintf(fid,'%s\n','];');

 %Exc.con
fprintf(fid,'%s\n','Exc.con = [...');
for i=1:size(mpc.exc,1)  %行数
    for j=1:size(mpc.exc,2)
        if mpc.exc(i,j)==fix(mpc.exc(i,j))
            fprintf(fid,'\t%d',mpc.exc(i,j));
        else
            fprintf(fid,'\t%f',mpc.exc(i,j));
        end
        if j==size(mpc.exc,2)
            fprintf(fid,'%s\n',';');
        end
    end
end
fprintf(fid,'%s\n','];');

%Bus.names
fprintf(fid,'%s\n','Bus.names = {...');
for i=1:size(mpc.busnames,1)  %行数
    fprintf(fid,'%s','''');
    fprintf(fid,'%s',mpc.busnames{i});
    fprintf(fid,'%s','''');
    fprintf(fid,'%s\n',';');
    
    
end
fprintf(fid,'%s\n','};');
    
fclose(fid);
   