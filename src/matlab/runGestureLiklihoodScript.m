g1 = {}
g2 = {}
g3 = {}
seq_g1_1 = {}
seq_g2_1 = {}
seq_g3_1 = {}
seq_g1_2 = {}
seq_g2_2 = {}
seq_g3_2 = {}
seq_g1_3 = {}
seq_g2_3 = {}
seq_g3_3 = {}
G1 = []
G2 = []
G3 = []
N1 = 20
N2 = 20
N3 = 20
M1 = 10
M2 = 10
M3 = 10

for i=1:N1
    g1{i} = load(sprintf('data/ges1_%g.txt', i));
    G1 = [G1; g1{i}];
end

for i=1:N2
    g2{i} = load(sprintf('data/ges2_%g.txt', i));
    G2 = [G2; g2{i}];
end

for i=1:N3
    g3{i} = load(sprintf('data/ges3_%g.txt', i));
    G3 = [G3; g3{i}];
end

C1 = csvread('../models/UD_obs.csv');
figure(1)
plot(G1(:,3), -G1(:,4), 'r.'); hold on; plot(C1(:,1), -C1(:,2), 'b*'); axis([-60 20 -60 20]); hold off

C2 = csvread('../models/LL_obs.csv');
figure(2)
plot(G2(:,3), -G2(:,4), 'r.'); hold on; plot(C2(:,1), -C2(:,2), 'b*'); axis([-40 100 -40 100]); hold off

C3 = csvread('../models/LR_obs.csv');
figure(3)
plot(G3(:,3), -G3(:,4), 'r.'); hold on; plot(C3(:,1), -C3(:,2), 'b*'); axis([-50 10 -50 10]); hold off

for i=1:N1
    [~, I] = min(pdist2(g1{i}(:, 3:4), C1)');
    seq_g1_1{i} = I;
    [~, I] = min(pdist2(g1{i}(:, 3:4), C2)');
    seq_g1_2{i} = I;
    [~, I] = min(pdist2(g1{i}(:, 3:4), C3)');
    seq_g1_3{i} = I;
end

for i=1:N2
    [~, I] = min(pdist2(g2{i}(:, 3:4), C1)');
    seq_g2_1{i} = I;
    [~, I] = min(pdist2(g2{i}(:, 3:4), C2)');
    seq_g2_2{i} = I;
    [~, I] = min(pdist2(g2{i}(:, 3:4), C3)');
    seq_g2_3{i} = I;
end

for i=1:N3
    [~, I] = min(pdist2(g3{i}(:, 3:4), C1)');
    seq_g3_1{i} = I;
    [~, I] = min(pdist2(g3{i}(:, 3:4), C2)');
    seq_g3_2{i} = I;
    [~, I] = min(pdist2(g3{i}(:, 3:4), C3)');
    seq_g3_3{i} = I;
end

K = 4;
a1 = csvread('../models/UD_a.csv');
b1 = csvread('../models/UD_b.csv');
p1 = csvread('../models/UD_p.csv');

figure(4)
for i=1:K
    subplot(1,K,i)
    plot(G1(:,3), -G1(:,4), 'g.');
    hold on;
    scatter(C1(:,1), -C1(:,2), 1000*b1(i,:)', [0,0,0]);
    axis([-20 20 -50 50]);
    hold off
end

K = 6;
a2 = csvread('../models/LL_a.csv');
b2 = csvread('../models/LL_b.csv');
p2 = csvread('../models/LL_p.csv');

figure(5)
for i=1:K
    subplot(K,1,i)
    plot(G2(:,3), -G2(:,4), 'g.');
    hold on;
    scatter(C2(:,1), -C2(:,2), 1000*b2(i,:)', [0,0,0]);
    axis([-40 100 -20 20]);
    hold off
end

K = 6;
a3 = csvread('../models/LR_a.csv');
b3 = csvread('../models/LR_b.csv');
p3 = csvread('../models/LR_p.csv');

figure(6)
for i=1:K
    subplot(K,1,i)
    plot(G3(:,3), -G3(:,4), 'g.');
    hold on;
    scatter(C3(:,1), -C3(:,2), 1000*b3(i,:)', [0,0,0]);
    axis([-50 10 -20 20]);
    hold off
end

disp('gesture 1')
for i=1:N1
    l11 = likelihood(a1,b1,p1,seq_g1_1(i));
    l12 = likelihood(a2,b2,p2,seq_g1_2(i));
    l13 = likelihood(a3,b3,p3,seq_g1_3(i));
    disp(sprintf('%g >> %g \t %g \t %g', i, l11, l12, l13))
end

disp('gesture 2')
for i=1:N2
    l21 = likelihood(a1,b1,p1,seq_g2_1(i));
    l22 = likelihood(a2,b2,p2,seq_g2_2(i));
    l23 = likelihood(a3,b3,p3,seq_g2_3(i));
    disp(sprintf('%g >> %g \t %g \t %g', i, l21, l22, l23))
end

disp('gesture 3')
for i=1:N3
    l31 = likelihood(a1,b1,p1,seq_g3_1(i));
    l32 = likelihood(a2,b2,p2,seq_g3_2(i));
    l33 = likelihood(a3,b3,p3,seq_g3_3(i));
    disp(sprintf('%g >> %g \t %g \t %g', i, l31, l32, l33))
end


%{
disp('others')
for i=1:6
    disp('--')
    q = randi(size(bigseq1,2)-40,1)
    cc1 = bigseq1(q:(q+27));
    cc2 = bigseq2(q:(q+27));
    TT = C(cc1',:);
    likelihood(a1,b1,p1,{cc1})
    likelihood(a2,b2,p2,{cc2})
end
%}

