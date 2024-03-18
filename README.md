# FIFO-FORK-e-PIPE
Desenvolva uma aplicação
cliente-servidor em C ou C++ para Linux com as seguintes características:

- O servidor deve rodar em 3 máquinas diferentes (Podem ser 3 terminais na mesma máquina) e cada grupo
vai providenciar uma base de dados diferente para cada um deles. O acesso a
cada servidor é por meio de sockets (TCP ou UDP).

O programa cliente vai fazer duas consultas diferentes:

 - Numa delas, o programa vai buscar a base toda consultando
todas as 3 máquinas.

 - Na outra, ele vai buscar uma informação determinada que deve
estar apenas em um dos 3 servidores, mas não necessariamente no primeiro. Ao
achar esta informação, o programa encerra sem procurar nos servidores
restantes.

Nos servidores, o grupo vai implementar o uso de  dos seguintes recursos existentes no Linux para comunicação entre processos: pipe, fifo e fork
