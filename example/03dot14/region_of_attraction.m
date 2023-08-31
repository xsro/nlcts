h1=figure();
hold on;
x=-3:0.01:3;
y=-3:0.01:3;
[X,Y]=meshgrid(x,y);
V=1.5*X.*X-X.*Y+Y.*Y;
Vd=-(X.*X+Y.*Y)-X.*X.*Y.*(X-2*Y);

colormap summer
contourf(X,Y,V,[0,0.3,0.618,2.25,4,6,9,12],'edgecolor','none')
colorbar;
contour(X,Y,V,[0.618,2.25],"ShowText",true,"LabelFormat","V=%g",'edgecolor','black')
contour(X,Y,Vd,[5,1,0],"r-","ShowText",true,"LabelFormat","V'=%g",'edgecolor','red')
axis equal 
axis([-2,2,-2,2])
xlabel('x1')
ylabel('x2')
% title("Contour of $V(x)$ and $V'=\dot{V}(x)$","Interpreter","latex")
%% print figure
%set(h1,'PaperSize',[10 10]); %set the paper size to what you want  
print(h1,'region_of_attraction_V','-dpdf',"-fillpage") % then print it


%%
load region_of_attraction.mat X Y T
h2=figure;  
hold on;
[x1,x2]=meshgrid(linspace(-3,3,1000));
streamslice(x1,x2, -x2, x1+(x1.^2-1).*x2);
axis([-3,3,-3,3])
grid on
xlabel('x1')
ylabel('x2')
axis equal
contour(X,Y,T>0,"LineWidth",2,"EdgeColor","black")
contour(X,Y,V,[0.618,2.25],"LineWidth",2,"ShowText",true,"LabelFormat","V=%g",'edgecolor','red')
%% print figure
set(h2,'PaperSize',[10 10]); %set the paper size to what you want  
print(h2,'region_of_attraction_esimate','-dpdf',"-fillpage") % then print it

return
%% 通过仿真得到实际的极限环绕
x=-3:0.01:3;
y=-3:0.01:3;
[X,Y]=meshgrid(x,y);
T=zeros(size(X));
for i=1:size(X,1)
    for j=1:size(X,2)
        x=X(i,j);y=Y(i,j);
        [t,x]=ode45(@f,[1 100],[x;y]);
        k=find(sqrt(x(:,1).^2+x(:,2).^2)<0.01);
        if ~isempty(k)
            T(i,j)=t(k(1));
        end
    end
end
save region_of_attraction.mat X Y T

%%
function dx=f(t,x)
    dx=[
        -x(2);x(1)+(x(1)^2-1)*x(2)
        ];

end