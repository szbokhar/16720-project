function [score] = likelihood(a, b, p, Xtest)
    N = numel(Xtest);
    Alpha = Forward(a, b, p, Xtest);

    score = zeros(N, 1);
    for n=1:N
        T = size(Xtest{n},2);
        score(n) = sum(Alpha{n}(T,:));
    end
    score = log(score);
end
