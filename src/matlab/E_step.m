function [Gamma, Xi] = E_step(a, b, p, X)
    N = numel(X);
    K = size(a,1);

    Gamma = cell(N,1);
    Xi = cell(N,1);

    Alpha = Forward(a,b,p,X);
    Beta = Backward(a,b,p,X);

    for n=1:N
        al = Alpha{n};
        be = Beta{n};
        den = sum(al.*be,2);
        x = X{n};

        T = size(X{n},2);
        ga = zeros(T,K);
        xi = zeros(T,K,K);
        for t=1:T
            for i=1:K
                ga(t,i) = (al(t,i)*be(t,i))/den(t);

                for j=1:K
                    if t > 1
                        xi(t,i,j) = (al(t-1,i)*a(i,j)*b(j,x(t))*be(t,j))/den(t);
                    end
                end
            end

        end

        Gamma{n} = ga;
        Xi{n} = xi;
    end
end
