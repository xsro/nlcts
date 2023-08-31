syms sigma;
right=2*sigma.^3./((1+sigma.*sqrt(sigma.^2+4)).*sqrt(4.*sigma.^2+(sigma.^2+1).^2));
s=latex(right);
sigma=0:0.01:10;
right=2*sigma.^3./((1+sigma.*sqrt(sigma.^2+4)).*sqrt(4.*sigma.^2+(sigma.^2+1).^2));
h=figure(1);hold on;
[m,i]=max(right);
plot(sigma,right,"-",sigma(i),m,"o")
xlabel("\sigma");
ylabel("RHS");
text(4,0.17,"$"+s+"$","Interpreter","latex","FontSize",18)
text(sigma(i)+0.5,m,sprintf("(%0.2f,%.4f)",sigma(i),m))
set(h,'PaperSize',[20 10]); %set the paper size to what you want  
print(h,'example_9dot4','-dpdf',"-fillpage") % then print it
