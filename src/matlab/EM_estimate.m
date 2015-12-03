function [a1,b1,p1] = EM_estimate(a, b, p, X, nIter)

    a1 = a;
    b1 = b;
    p1 = p;
    for i=1:nIter
        [Ga, Xi] = E_step(a1,b1,p1,X);
        [a1, b1, p1] = M_step(Ga, Xi, X, size(b,2), size(b,1));
    end

end
