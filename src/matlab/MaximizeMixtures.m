function [t] = MaximizeMixtures(k, w)
    t = sum(w,1)'/sum(sum(w,1));
end
