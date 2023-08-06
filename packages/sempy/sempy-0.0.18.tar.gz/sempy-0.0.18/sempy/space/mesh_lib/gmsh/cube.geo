// Gmsh project created on Sun Apr 25 14:13:04 2010

Mesh.ElementOrder = 2;
Mesh.SecondOrderLinear = 0;

lc = 0.5;//1.0;//0.125;
//lc = 0.25;
//lc = 0.125;
//lc = 0.0625;

Point(1) = {0, 0, 0, lc};
Point(2) = {1, 0, 0, lc};
Point(3) = {1, 1, 0, lc};
Point(4) = {0, 1, 0, lc};

Point(5) = {0, 0, 1, lc};
Point(6) = {1, 0, 1, lc};
Point(7) = {1, 1, 1, lc};
Point(8) = {0, 1, 1, lc};

Line(1) = {5, 6};
Line(2) = {6, 7};
Line(3) = {7, 8};
Line(4) = {8, 5};
Line(5) = {6, 2};
Line(6) = {2, 1};
Line(7) = {1, 5};
Line(8) = {2, 3};
Line(9) = {3, 7};
Line(10) = {3, 4};
Line(11) = {4, 8};
Line(12) = {4, 1};
Line Loop(13) = {1, 2, 3, 4};
Plane Surface(14) = {13};
Line Loop(15) = {5, 8, 9, -2};
Plane Surface(16) = {15};
Line Loop(17) = {1, 5, 6, 7};
Plane Surface(18) = {17};
Line Loop(19) = {4, -7, -12, 11};
Plane Surface(20) = {19};
Line Loop(21) = {3, -11, -10, 9};
Plane Surface(22) = {21};
Line Loop(23) = {6, -12, -10, -8};
Plane Surface(24) = {23};
Surface Loop(25) = {14, 18, 16, 24, 20, 22};
Volume(26) = {25};
Physical Surface("Dirichlet 1") = {14};
Physical Surface("Dirichlet 2") = {16, 24, 20, 18, 22};
Physical Volume("Solid") = {26};
