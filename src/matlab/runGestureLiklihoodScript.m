g1 = {}
g2 = {}
g3 = {}
g4 = {}
seq_g1 = {}
seq_g2 = {}
seq_g3 = {}
seq_g4 = {}
G1 = []
G2 = []
G3 = []
G4 = []
N1 = 20
N2 = 20
N3 = 20
N4 = 53
M1 = 10
M2 = 10
M3 = 10
Mall = 20
M1 = Mall
M2 = Mall
M3 = Mall

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

for i=1:N4
    g4{i} = load(sprintf('data/gesNon_%g.txt', i));
    G4 = [G4; g4{i}];
end

C = csvread('../models/4hmmUD_obs.csv');
figure(1)
A = [G1; G2; G3; G4];
plot(A(:,3), -A(:,4), 'r.'); hold on; plot(C(:,1), -C(:,2), 'b*'); hold off

for i=1:N1
    [~, I] = min(pdist2(g1{i}(:, 3:4), C)');
    seq_g1{i} = I;
end

for i=1:N2
    [~, I] = min(pdist2(g2{i}(:, 3:4), C)');
    seq_g2{i} = I;
end

for i=1:N3
    [~, I] = min(pdist2(g3{i}(:, 3:4), C)');
    seq_g3{i} = I;
end

for i=1:N4
    [~, I] = min(pdist2(g4{i}(:, 3:4), C)');
    seq_g4{i} = I;
end

K = 4;
a1 = csvread('../models/4hmmUD_a.csv');
b1 = csvread('../models/4hmmUD_b.csv');
p1 = csvread('../models/4hmmUD_p.csv');

figure(2)
for i=1:K
    subplot(1,K,i)
    plot(G1(:,3), -G1(:,4), 'g.');
    hold on;
    scatter(C1(:,1), -C1(:,2), 1000*b1(i,:)', [0,0,0]);
    axis([-20 20 -50 50]);
    hold off
end

K = 6;
a2 = csvread('../models/4hmmLL_a.csv');
b2 = csvread('../models/4hmmLL_b.csv');
p2 = csvread('../models/4hmmLL_p.csv');

figure(3)
for i=1:K
    subplot(K,1,i)
    plot(G2(:,3), -G2(:,4), 'g.');
    hold on;
    scatter(C2(:,1), -C2(:,2), 1000*b2(i,:)', [0,0,0]);
    axis([-40 100 -20 20]);
    hold off
end

K = 6;
a3 = csvread('../models/4hmmLR_a.csv');
b3 = csvread('../models/4hmmLR_b.csv');
p3 = csvread('../models/4hmmLR_p.csv');

figure(4)
for i=1:K
    subplot(K,1,i)
    plot(G3(:,3), -G3(:,4), 'g.');
    hold on;
    scatter(C3(:,1), -C3(:,2), 1000*b3(i,:)', [0,0,0]);
    axis([-50 10 -20 20]);
    hold off
end

K = 4;
a4 = csvread('../models/4hmmNO_a.csv');
b4 = csvread('../models/4hmmNO_b.csv');
p4 = csvread('../models/4hmmNO_p.csv');

figure(5)
for i=1:K
    subplot(K,1,i)
    plot(A(:,3), -A(:,4), 'g.');
    hold on;
    scatter(C(:,1), -C(:,2), 1000*b3(i,:)', [0,0,0]);
    hold off
end

disp('gesture 1')
for i=1:N1
    l11 = likelihood(a1,b1,p1,seq_g1_1(i));
    l12 = likelihood(a2,b2,p2,seq_g1_2(i));
    l13 = likelihood(a3,b3,p3,seq_g1_3(i));
    l14 = likelihood(a4,b4,p4,seq_g1_3(i));
    [~,j] = max([l11,l12,l13,l14]);
    disp(sprintf('%g >> %g \t %g \t %g \t %g \t %g', i, l11, l12, l13, l14, j))
end

disp('gesture 2')
for i=1:N2
    l21 = likelihood(a1,b1,p1,seq_g2_1(i));
    l22 = likelihood(a2,b2,p2,seq_g2_2(i));
    l23 = likelihood(a3,b3,p3,seq_g2_3(i));
    l24 = likelihood(a4,b4,p4,seq_g2_3(i));
    [~,j] = max([l21,l22,l23,l24]);
    disp(sprintf('%g >> %g \t %g \t %g \t %g \t %g', i, l21, l22, l23, l24, j))
end

disp('gesture 3')
for i=1:N3
    l31 = likelihood(a1,b1,p1,seq_g3_1(i));
    l32 = likelihood(a2,b2,p2,seq_g3_2(i));
    l33 = likelihood(a3,b3,p3,seq_g3_3(i));
    l34 = likelihood(a4,b4,p4,seq_g3_3(i));
    [~,j] = max([l31,l32,l33,l34]);
    disp(sprintf('%g >> %g \t %g \t %g \t %g \t %g', i, l31, l32, l33, l34, j))
end

disp('No gesture')
for i=1:N4
    l41 = likelihood(a1,b1,p1,seq_g4(i));
    l42 = likelihood(a2,b2,p2,seq_g4(i));
    l43 = likelihood(a3,b3,p3,seq_g4(i));
    l44 = likelihood(a4,b4,p4,seq_g4(i));
    [~,j] = max([l41,l42,l43,l44]);
    disp(sprintf('%g >> %g \t %g \t %g \t %g \t %g', i, l41, l42, l43, l44, j))
end
