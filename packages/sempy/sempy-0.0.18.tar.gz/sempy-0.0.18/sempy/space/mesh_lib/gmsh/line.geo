// Gmsh project created on Sun Apr 25 14:13:04 2010

Mesh.ElementOrder = 2;
Mesh.SecondOrderLinear = 0;

lc1 = 0.4;//0.2;//0.3;
lc2 = 0.4;//0.02;//0.05;

Point(1) = {0, 0, 0, lc1};
Point(2) = {1.0, 0, 0, lc2};

Line(1) = {1, 2};

Physical Point("Dir 1") = {1};
Physical Point("Dir 2") = {2};

Physical Line("Solid") = {1};

//Physical Line("Dirichlet 1") = {1};
