# Rubrica — mensagem de commit escrita pelo agente

Critérios sim/não. Nunca nota de 1 a 10. (invariável) = um "nao" reprova a mensagem, independente do resto.
O que dá para checar por código (tamanho da 1ª linha, formato) NÃO entra aqui: vai para um teste.

R1 | A mensagem diz POR QUE a mudança foi feita, não só o que mudou? | qualidade
R2 | Toda MUDANÇA que a mensagem cita está no diff (não inventa arquivo, teste nem efeito)? O motivo pode vir de fora do diff. | invariável
R3 | Quem não viu o diff entende o que mudou só pela mensagem? | qualidade
