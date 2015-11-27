function [sigma] = MaximizeCovariance(X, k, w, mu)
    sigma = [];
    N_k = sum(w,1);
    f = size(X,2);
    n = size(X,1);
    for j=1:k
        nX = sqrt(repmat(w(:,j), [1,f])) .* (X - repmat(mu(j,:), [n,1]));

        tmp = (1/N_k(j))*nX'*nX;
        sigma(:,:,j) = tmp;
    end
end

