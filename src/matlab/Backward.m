function [Beta] = Backward(a, b, p, X)
    N = numel(X);
    K = size(a,1);
    Beta = cell(N,1);

    for n=1:N
        x = X{n};
        T = size(x,2);
        B = zeros(T,K);
        B(T,:) = ones(1,K);

        for t=(T-1):-1:1
            B(t,:) = a*(b(:,x(t+1)).*B(t+1,:)');
        end
        Beta{n} = B;
    end
end
