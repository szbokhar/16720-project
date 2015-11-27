function [mu] = MaximizeMean(X, k, w)
    mu = [];
    f = size(X,2);
    N_k = sum(w,1);
    for j=1:k
        tmp = (1/N_k(j))*sum(repmat(w(:,j), [1,f]) .* X);
        mu = [mu; tmp];
    end
end
