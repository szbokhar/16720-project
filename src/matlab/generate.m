function [x] = generate(a, b, p, T)
    x = zeros(1,T);
    state = (rand(1) > p(1)) + 1;

    for t=1:T
        x(t) = (rand(1) > b(state,1)) + 1;
        state = (rand(1) > a(state,1)) + 1;
    end
end
