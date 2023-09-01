% example for equestion in 3 stability
% Why do we need the radial unboundedness condition to show global asymptotic stability?

h4=figure;

x=-8:0.01:8;
y=-3:0.01:3;
[X,Y]=meshgrid(x,y);
V=X.*X./(1+X.*X)+Y.*Y;
contourf(X,Y,V,[0.1,0.5,1,2,4,6,9,12],"ShowText",true,"LabelFormat",@mylabelfun)
axis equal
colormap summer
xlabel("x_1")
ylabel("x_2")
set(h4,'PaperSize',[20 10]); %set the paper size to what you want  
print(h4,'lyapunov_function','-dpdf',"-fillpage") % then print it

function labels = mylabelfun(vals)
labels = vals ;
labels(vals == 0) = "0 m";
end