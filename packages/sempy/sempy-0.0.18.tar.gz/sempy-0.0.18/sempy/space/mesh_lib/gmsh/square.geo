// Gmsh project created on Sun Apr 25 14:13:04 2010

Mesh.ElementOrder = 2;
Mesh.SecondOrderLinear = 0;

lc1 = 0.5;
lc2 = 0.5;
lc3 = 0.5;

Point(1) = {0, 0, 0, lc1};
Point(2) = {1, 0, 0, lc2};
Point(3) = {1, 1, 0, lc3};
Point(4) = {0, 1, 0, lc2};

Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};
Line Loop(5) = {1, 2, 3, 4};
Plane Surface(6) = {5};


//Physical Line("Dirichlet") = {3, 2, 1, 4};
Physical Line("Dirichlet 1") = {1};
Physical Line("Dirichlet 2") = {2};
Physical Line("Dirichlet 3") = {3};
Physical Line("Dirichlet 4") = {4};
Physical Surface("Internal") = {6};
