% unfinished
[t,x]=ode45(@rhs,[0,0.5],[1,-0.5]);
plot(t,x(:,1))
xlim([0,0.5])

function dx=rhs(t,x)
    a=0.25;b=0.2;
    dx=[
        x(2);
        -x(1)-2*x(2)+a*x(1)^2*x(2)+b*sin(2*t)
        ];
end