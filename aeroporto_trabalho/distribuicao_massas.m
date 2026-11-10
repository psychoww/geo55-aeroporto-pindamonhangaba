function distribuicao_massas(csv, Fh, Dext, saida, DextEco)
%DISTRIBUICAO_MASSAS Linhas de compensação, bota-fora/empréstimo e momento de transporte da PPD.
%   Usa as funções do programa da aula de 20/10 (../diagrama_massas/dm_*.m), com as mesmas
%   convenções: a LC compensa só entre seus cruzamentos com o diagrama; o que fica fora é
%   material externo (bota-fora ou empréstimo) levado à DMT externa Dext.
%
%   csv      memorial no formato do programa (Ponto;Distancia;Corte;Aterro, áreas em m²)
%   Fh       fator de homogeneização
%   Dext     DMT de bota-fora e empréstimo da aula (m)
%   saida    JSON com os resultados
%   DextEco  variante com o custo de escavar o empréstimo (DMT equivalente, m)
%
%   Rodar: matlab -batch "distribuicao_massas('Tabelas/entrada_diagrama_massas.csv', 1.25, 150, 'dados/distribuicao.json', 1150)"

aqui = fileparts(mfilename('fullpath'));
addpath(fullfile(aqui, '..', 'diagrama_massas'));
T = readtable(csv, 'Delimiter', ';', 'DecimalSeparator', ',', 'VariableNamingRule', 'preserve');
x = T{:, 2}; c = T{:, 3}; a = T{:, 4};
M = dm_calcular(x, c, a, Fh, 0, "areas");
O = M.O;

R = struct();
R.Fh = Fh; R.Dext = Dext; R.DextEco = DextEco;
R.x = x; R.O = O;
R.Vc = sum(M.volC(2:end)); R.Va = sum(M.volA(2:end)); R.VaCorr = sum(M.volAc(2:end));

% B) LC única ótima
[y1, ~] = dm_otimizar_unica(x, O, Dext);
S1 = dm_ajustar_lc(x, O, [x(1) x(end) y1]);
R.cenarios.lc_unica = resumo(x, O, S1, Dext, 'LC única ótima, entre cruzamentos (convenção do exercício 2)');

% C) Várias LCs (até 6) e livre: programação dinâmica do programa
[~, ~, porN] = dm_otimizar_degraus(x, O, Dext, 6);
R.porN = arrayfun(@(p) struct('n', p.n, 'MT', p.MT / 10), porN);
for n = [2 3 4 6]
    R.cenarios.(sprintf('ate_%d_lcs', n)) = resumo(x, O, porN(n).S, Dext, sprintf('Até %d LCs', n));
end
[Sl, ~] = dm_otimizar_degraus(x, O, Dext, Inf);
R.cenarios.livre = resumo(x, O, Sl, Dext, 'LCs livres (ótimo global)');

% D) Variante: o empréstimo custa também a escavação (DMT externa equivalente DextEco)
[Se, ~] = dm_otimizar_degraus(x, O, DextEco, Inf);
R.cenarios.eco = resumo(x, O, Se, DextEco, sprintf('LCs livres com DMT externa equivalente de %g m', DextEco));
R.cenarios.eco_aula = resumo(x, O, Se, Dext, 'Solução da variante, medida com a DMT da aula');

fid = fopen(saida, 'w', 'n', 'UTF-8'); fprintf(fid, '%s', jsonencode(R, 'PrettyPrint', true)); fclose(fid);
nomes = fieldnames(R.cenarios);
for k = 1:numel(nomes)
    s = R.cenarios.(nomes{k});
    fprintf('%-55s MT = %12.0f m3.dam  (int %10.0f, ext %10.0f)  BF %9.0f  EMP %9.0f  LCs %d\n', ...
        s.nome, s.MT, s.MTint, s.MText, s.Vbf, s.Vemp, size(s.S, 1));
end
end

function s = resumo(x, O, S, D, nome)
r = dm_momento(x, O, S, D);
s.nome = nome;
s.S = S;
s.MT = r.MT / 10; s.MTint = r.MTint / 10; s.MText = r.MText / 10;   % m³·dam
s.MTmeia = r.MTmeia / 10;
s.Vbf = r.Vbf; s.Vemp = r.Vemp;
s.ondas = arrayfun(@(w) struct('ini', w.ini, 'fim', w.fim, 'sinal', w.sinal, 'V', w.V, 'DMT', w.DMT, ...
    'DMTmeia', w.DMTmeia, 'MT', w.MT / 10, 'xpk', w.xpk, 'ypk', w.ypk, 'lpk', w.lpk), r.ondas);
s.ext = arrayfun(@(e) struct('tipo', char(e.tipo), 'de', e.de, 'ate', e.ate, 'V', e.V), r.ext);
s.Vint = sum([r.ondas.V]);
s.DMTmedia = r.MTint / max(s.Vint, eps);
end
