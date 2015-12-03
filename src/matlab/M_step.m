function [a, b, p] = M_step(Gamma, Xi, X, M, K)

    N = numel(X);

    B = zeros(K,M);
    nn = zeros(K,K);
    init = zeros(K,1);

    for k=1:K
        for j=1:M
            B(k,j) = 0.1;
            for n=1:N
                x = X{n};
                B(k,j) = B(k,j) + sum(Gamma{n}(x==j,k));
            end
        end
    end

    for i=1:K
        for j=1:K
            % nn(i,j) = 1;
            for n=1:N
                nn(i,j) = nn(i,j) + sum(Xi{n}(:,i,j));
            end
        end
    end

    for n=1:N
        init = init + Gamma{n}(1,:)';
    end

    a = bsxfun(@rdivide, nn, sum(nn,2));
    b = bsxfun(@rdivide, B, sum(B,2));
    p = init/sum(init);
end
