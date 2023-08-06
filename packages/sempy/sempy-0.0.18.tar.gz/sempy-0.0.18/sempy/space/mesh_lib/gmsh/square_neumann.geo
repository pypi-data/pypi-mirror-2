// Gmsh project created on Sun Apr 25 14:13:04 2010

Mesh.ElementOrder = 2;
Mesh.SecondOrderLinear = 0;

lc = 0.5;

Point(1) = {0, 0, 0, lc};
Point(2) = {1, 0, 0, lc};
Point(3) = {1, 1, 0, lc};
Point(4) = {0, 1, 0, lc};

Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};
Line Loop(5) = {1, 2, 3, 4};
Plane Surface(6) = {5};


Physical Line("Dirichlet") = {1, 2};
Physical Line("Neumann") = {4, 3};
Physical Surface(9) = {6};
