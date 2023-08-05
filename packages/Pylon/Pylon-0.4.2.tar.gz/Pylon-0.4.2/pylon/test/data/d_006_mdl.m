Bus.con = [ ... 
1  400    1    0    2    1;
2  400    1    0    2    1;
3  400    1    0    2    1;
4  400    1    0    2    1;
5  400    1    0    2    1;
6  400    1    0    2    1;
 ];

Line.con = [ ... 
2             3           100           400            60             0             0          0.05          0.25          0.06             0             0        0.3082             0             0             1;
3             6           100           400            60             0             0          0.02           0.1          0.02             0             0        1.3973             0             0             1;
4             5           100           400            60             0             0           0.2           0.4          0.08             0             0        0.1796             0             0             1;
3             5           100           400            60             0             0          0.12          0.26          0.05             0             0        0.6585             0             0             1;
5             6           100           400            60             0             0           0.1           0.3          0.06             0             0           0.2             0             0             1;
2             4           100           400            60             0             0          0.05           0.1          0.02             0             0         1.374             0             0             1;
1             2           100           400            60             0             0           0.1           0.2          0.04             0             0        0.2591             0             0             1;
1             4           100           400            60             0             0          0.05           0.2          0.04             0             0        0.9193             0             0             1;
1             5           100           400            60             0             0          0.08           0.3          0.06             0             0        0.8478             0             0             1;
2             6           100           400            60             0             0          0.07           0.2          0.05             0             0        0.9147             0             0             1;
2             5           100           400            60             0             0           0.1           0.3          0.04             0             0        0.7114             0             0             1;
 ];

SW.con = [ ... 
2           100           400          1.05             0           1.5          -1.5           1.1           0.9           1.4             1;
 ];

PV.con = [ ... 
1           100           400           0.9          1.05           1.5          -1.5           1.1           0.9             1             1;
3           100           400           0.6          1.05           1.5          -1.5           1.1           0.9             1             1;
 ];

PQ.con = [ ... 
4           100           400           0.9           0.6           1.1           0.9             0             1;
5           100           400             1           0.7           1.1           0.9             0             1;
6           100           400           0.9           0.6           1.1           0.9             0             1;
 ];

Demand.con = [ ... 
6           100           0.2      0.066666           0.2         1e-05             0             0           9.5             0             0             0             0             0             0             0             0             1;
5           100           0.1          0.07           0.1         1e-05             0             0          10.5             0             0             0             0             0             0             0             0             1;
4           100          0.25      0.166665          0.25         1e-05             0             0            12             0             0             0             0             0             0             0             0             1;
 ];

Supply.con = [ ... 
1           100           0.2           0.2         1e-05             0             0           9.7             0             0             0             0             0             0             1           1.5          -1.5             0             0             1;
2           100          0.25          0.25         1e-05             0             0           8.8             0             0             0             0             0             0             1           1.5          -1.5             0             0             1;
3           100          0.22           0.2         1e-05             0             0             7             0             0             0             0             0             0             1           1.5          -1.5             0             0             1;
 ];

Varname.bus = {... 
'Bus1'; 'Bus2'; 'Bus3'; 'Bus4'; 'Bus5'; 
'Bus6'};
