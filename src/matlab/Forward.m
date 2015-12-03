function [Alpha] = Forward(a, b, p, X)
    N = numel(X);
    K = size(a,1);
    Alpha = cell(N,1);

    for n=1:N
        x = X{n};
        T = size(x,2);
        A = zeros(T,K);
        A(1,:) = (b(:,x(1)).*p)';

        for t=2:T
            A(t,:) = A(t-1,:)*a.*b(:,x(t))';
        end
        Alpha{n} = A;
    end
end
