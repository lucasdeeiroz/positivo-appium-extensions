# Network Status — AppiumLibrary Extension

`NetworkStatus` é uma keyword personalizada desenvolvida para facilitar a leitura do status de rede em dispositivos Android durante testes com Appium + Robot Framework. Ela utiliza a propriedade `driver.network_connection` para identificar o tipo de conexão de rede de um dispositivo Android e retornar uma string legível.

---

## Objetivo

- Interpretar de forma clara e confiável as informações recebidas através de `bitmasks`
- Entregar uma resposta legível do tipo de conexão de rede ativa (Wi‑Fi, dados móveis, modo avião ou nenhum)
- Validar se o dispositivo está com rede antes de executar testes que exigem conexão
- Garantir que um cenário offline está devidamente configurado
- Diferenciar se a conexão está vindo de dados móveis ou Wi-Fi
- Tornar os testes mais robustos em diferentes dispositivos e emuladores

---

## Como Funciona

O método `driver.network_connection` do Appium retorna um número inteiro com bits ativados conforme o tipo de conexão:

| Valor | Tipo de Conexão          |
|-------|--------------------------|
| 0     | Nenhuma conexão          |
| 1     | Modo avião               |
| 2     | Apenas Wi‑Fi             |
| 4     | Apenas dados móveis      |
| 6     | Wi‑Fi + dados móveis     |

A keyword consulta o modo avião via ADB (`adb shell settings get global airplane_mode_on`) e dá prioridade a ele quando ativado, mesmo com Wi-Fi e dados ativados.
Além disso, também tem um fallback final (retornando `UNKNOWN`) que serve para cobrir erro de leitura do bitmask ou possíveis anomalias no valor do status obtido.
Dessa forma, interpreta esses valores e retorna uma string legível como:

[nenhuma conexão?] → `NONE`
[modo avião?] → `AIRPLANE_MODE`
[apenas Wi-Fi?] → `WIFI_ONLY`
[apenas dados móveis?] → `DATA_ONLY`
[Wi-Fi + dados móveis?] → `WIFI_AND_DATA`
[não caiu em nada?] → `UNKNOWN`

---

## Como Executar

Para executar os testes:

```bash
robot NetworkStatus.robot
```

Caso queira executar testes de tags específicas:

```bash
robot -i tag NetworkStatus.robot
```

Certifique-se de que:
- O `AppiumLibrary` e a keyword `NetworkStatus`estão importadas corretamente
- O emulador/dispositivo está online

---

## Detalhes Técnicos

- Compatível com AppiumLibrary para Robot Framework
- Usa `driver.network_connection`
- A keyword foi projetada para ser simples, confiável e fácil de manter

---

## Estrutura do Código

- Escrita como uma classe (NetworkStatus) com ROBOT_LIBRARY_SCOPE = GLOBAL
- Modularizada com subfunções auxiliares (`interpretar_bitmask`, `definir_status_rede`, etc.)
- Não exige parâmetros e não realiza validações complexas
- A leitura de modo avião é feita por ADB, garantindo maior precisão

---

## Estrutura dos Testes

A keyword já foi testada nos seguintes cenários:

### Testes mockados

- **Sem rede (NONE) - bitmask: 0**
- **Modo avião ativado (AIRPLANE_MODE) - bitmask: 1**
- **Wi-Fi ativo - bitmask: 2**
- **Dados móveis ativos - bitmask: 4**
- **Wi-Fi e dados ativos - bitmask: 6**
- **Bitmask desconhecido (UNKNOWN) - bitmask: 8**

### Testes em emulador

- **Status Com Apenas Wi-Fi Ativo**
- **Status Com Apenas Dados Móveis Ativos**
- **Status Com Wi-Fi E Dados Ativos**
- **Status Em Modo Avião (com wi-fi e dados desativados)**
- **Status Sem Conexão Ativa**
- **Status Modo Avião com WI-Fi Ligado**

### Testes em dispositivo físico (ainda não realizados)

- **Status Com Apenas Wi-Fi Ativo**
- **Status Com Apenas Dados Móveis Ativos**
- **Status Com Wi-Fi E Dados Ativos**
- **Status Em Modo Avião (com wi-fi e dados desativados)**
- **Status Sem Conexão Ativa**
- **Status Modo Avião com WI-Fi Ligado**
- **Status Modo avião com Dados Ligados**