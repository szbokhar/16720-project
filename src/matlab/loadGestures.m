g1 = {}
g2 = {}
g3 = {}
g4 = {}
seq_g1_1 = {}
seq_g2_1 = {}
seq_g3_1 = {}
seq_g1_2 = {}
seq_g2_2 = {}
seq_g3_2 = {}
seq_g1_3 = {}
seq_g2_3 = {}
seq_g3_3 = {}
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

A = [G1; G2; G3; G4];
[clusAll,C] = kmeans(A(:, 3:4), Mall)
figure(4)
plot(A(:,3), -A(:,4), 'r.'); hold on; plot(C(:,1), -C(:,2), 'b*'); hold off
C1 = C;
C2 = C;
C3 = C;

%{
A = load('data/obsdata.txt');
[~, bigseq1] = min(pdist2(A(:, 3:4), C1)');
[~, bigseq2] = min(pdist2(A(:, 3:4), C2)');
%}

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

for i=1:N4
    [~, I] = min(pdist2(g4{i}(:, 3:4), C)');
    seq_g4{i} = I;
end

K = 4;
a0 = eye(K) + circshift(eye(K), [0,1]); a0(end,1)=0; a0 = bsxfun(@rdivide, a0, sum(a0, 2));
b0 = rand(K,M1)/M1; b0 = bsxfun(@rdivide, b0, sum(b0, 2));
p0 = zeros(K,1);
p0(1) = 1;

[a1, b1, p1] = EM_estimate(a0, b0, p0, seq_g1_1, 700)

figure(5)
for i=1:K
    subplot(1,K,i)
    plot(G1(:,3), -G1(:,4), 'g.');
    hold on;
    scatter(C1(:,1), -C1(:,2), 1000*b1(i,:)', [0,0,0]);
    axis([-20 20 -50 50]);
    hold off
end

K = 6;
a0 = eye(K) + circshift(eye(K), [0,1]); a0(end,1)=0; a0 = bsxfun(@rdivide, a0, sum(a0, 2));
b0 = rand(K,M2)/M2; b0 = bsxfun(@rdivide, b0, sum(b0, 2));
p0 = zeros(K,1);
p0(1) = 1;

[a2, b2, p2] = EM_estimate(a0, b0, p0, seq_g2_2, 700)

figure(6)
for i=1:K
    subplot(K,1,i)
    plot(G2(:,3), -G2(:,4), 'g.');
    hold on;
    scatter(C2(:,1), -C2(:,2), 1000*b2(i,:)', [0,0,0]);
    axis([-40 100 -20 20]);
    hold off
end

K = 6;
a0 = eye(K) + circshift(eye(K), [0,1]); a0(end,1)=0; a0 = bsxfun(@rdivide, a0, sum(a0, 2));
b0 = rand(K,M3)/M3; b0 = bsxfun(@rdivide, b0, sum(b0, 2));
p0 = zeros(K,1);
p0(1) = 1;

[a3, b3, p3] = EM_estimate(a0, b0, p0, seq_g3_3, 700)

figure(7)
for i=1:K
    subplot(K,1,i)
    plot(G3(:,3), -G3(:,4), 'g.');
    hold on;
    scatter(C3(:,1), -C3(:,2), 1000*b3(i,:)', [0,0,0]);
    axis([-50 10 -20 20]);
    hold off
end

K = 4;
a0 = eye(K) + circshift(eye(K), [0,1]); a0(end,1)=0; a0 = bsxfun(@rdivide, a0, sum(a0, 2));
b0 = rand(K,Mall)/Mall; b0 = bsxfun(@rdivide, b0, sum(b0, 2));
p0 = zeros(K,1);
p0(1) = 1;

[a4, b4, p4] = EM_estimate(a0, b0, p0, [seq_g4], 700)

figure(8)
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
