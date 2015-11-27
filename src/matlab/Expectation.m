function [w] = Expectation(X, k, t, mu, sigma)
    n = size(X,1);
    w = [];
    for j=1:k
        tmp = mvnpdf(X, mu(j,:), sigma(:,:,j)) * t(j);
        w = [w, tmp];
    end
    w = w ./ repmat(sum(w,2), [1,k]);
end
