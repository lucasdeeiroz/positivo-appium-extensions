# Repositório de Keywords para Robot Framework e Appium (Android)

<div align="center">

![Robot Framework](https://img.shields.io/badge/Robot%20Framework-4.0+-00A989?style=for-the-badge&logo=robot-framework&logoColor=white)
![Appium](https://img.shields.io/badge/Appium-2.0+-662d91?style=for-the-badge&logo=appium&logoColor=white)
![Android](https://img.shields.io/badge/Android-7.0+-3DDC84?style=for-the-badge&logo=android&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)

</div>

Este repositório contém uma coleção de keywords personalizadas para estender as funcionalidades do Robot Framework e AppiumLibrary, otimizadas especificamente para automação de testes em aplicações móveis Android. Cada keyword foi desenvolvida para resolver problemas específicos de interação com elementos de UI, proporcionando maior estabilidade, precisão e confiabilidade nos testes automatizados.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Keywords Disponíveis](#keywords-disponíveis)
  - [ChangeTheme](#changetheme)
  - [TerminateApplication](#terminateapplication)
  - [ClickElementV2](#clickelementv2)
  - [Click Elements](#click-elements)
  - [Compare Images](#compare-images)
  - [Get Network Connection Status](#get-network-connection-status)
  - [Get Visible Elements On Screen](#get-visible-elements-on-screen)
  - [Long Press V2](#long-press-v2)
  - [Pinch](#pinch)
  - [Scroll](#scroll)
  - [Scroll To Element](#scroll-to-element)
  - [Swipe](#swipe)
  - [Tap At Percentage](#tap-at-percentage)
  - [Wait Multiple Elements](#wait-multiple-elements)
  - [Zoom](#zoom)
- [Como Contribuir](#como-contribuir)
- [Licença](#licença)

## Visão Geral

Este repositório contém keywords personalizadas para o Robot Framework com foco exclusivo em automação de testes móveis para dispositivos Android usando Appium. As keywords foram meticulosamente projetadas para facilitar interações complexas com elementos de UI, como gestos multi-touch, scrolls precisos, verificações de visibilidade de elementos, e manipulação avançada de estados de aplicação.

As keywords deste repositório resolvem desafios comuns enfrentados durante a automação de testes em aplicativos Android, como:

- Inconsistências na detecção e interação com elementos de UI
- Dificuldades na implementação de gestos complexos (pinch, zoom, swipe)
- Problemas de sincronização durante carregamento de telas e elementos
- Limitações nas capacidades nativas do AppiumLibrary
- Necessidade de interações mais precisas e confiáveis com a interface do usuário

## Pré-requisitos

### Ambiente de Desenvolvimento

- Python 3.7+ (recomendado Python 3.9 ou superior)
- Robot Framework 4.0+ (`pip install robotframework`)
- AppiumLibrary para Robot Framework (`pip install robotframework-appiumlibrary`)
- OpenCV para Python (`pip install opencv-python`)
- NumPy (`pip install numpy`)
- scikit-image para comparação de imagens (`pip install scikit-image`)

### Configuração do Appium

- Appium Server 2.0+ (recomendado a versão mais recente)
- Appium UiAutomator2 Driver para Android
- Java JDK 8 ou superior (para o servidor Appium)
- Android SDK Platform Tools (para ADB)

### Dispositivos Suportados

- Dispositivos Android físicos (Android 7.0 Nougat ou superior)
- Emuladores Android (Android 7.0 Nougat ou superior)
- Recomendado: Android 10+ para melhor compatibilidade com gestos avançados

### Configurações Adicionais

- Modo de desenvolvedor ativado nos dispositivos Android
- Depuração USB ativada
- Permissões de sobreposição de tela para capturas de screenshot
- Configurações de acessibilidade para automação

## Instalação

### 1. Configuração do Ambiente

#### Instalação do Python e Dependências

```bash
# Instale o Python (caso ainda não tenha instalado)
# Recomendamos Python 3.9 ou superior

# Instale o pip (gerenciador de pacotes do Python)
python -m ensurepip --upgrade

# Atualize o pip para a versão mais recente
python -m pip install --upgrade pip
```

#### Instalação do Appium

```bash
# Instale o Appium via npm
npm install -g appium

# Instale o driver UiAutomator2 para Android
appium driver install uiautomator2

# Verifique a instalação
appium driver list
```

### 2. Clone este Repositório

```bash
git clone https://github.com/seu-usuario/robot-framework-front.git
cd robot-framework-front
```

### 3. Instale as Dependências do Projeto

```bash
pip install -r requirements.txt
```

### 4. Configuração do Dispositivo Android

1. Ative o modo de desenvolvedor no dispositivo Android:
   - Vá para **Configurações > Sobre o telefone**
   - Toque 7 vezes em **Número da versão**

2. Ative a depuração USB:
   - Vá para **Configurações > Opções do desenvolvedor**
   - Ative **Depuração USB**

3. Conecte o dispositivo ao computador e aceite a solicitação de depuração USB

4. Verifique se o dispositivo está sendo reconhecido:
   ```bash
    adb devices
   ```

### 5. Iniciar o Servidor Appium

```bash
# Inicie o servidor Appium em um terminal separado
appium
```

## Keywords Disponíveis

### ChangeTheme

Keyword personalizada para alternar entre temas claro e escuro em aplicativos Android durante a execução de testes automatizados. Esta keyword facilita o teste de compatibilidade visual e funcional da aplicação em diferentes modos de tema.

**Principais funcionalidades:**
- Alternar programaticamente entre temas claro e escuro durante a execução do teste
- Verificar a compatibilidade da UI em diferentes configurações de tema
- Testar a persistência de configurações de tema entre sessões
- Validar a adaptação correta de elementos visuais em diferentes temas

**Compatibilidade:**
- Android 7.0 (Nougat) ou superior
- Funcionalidade completa em Android 10+ com suporte nativo a tema escuro

**Exemplo de uso:**
```robot
# Alternar para tema escuro
Change Theme    dark

# Alternar para tema claro
Change Theme    light

# Verificar tema atual
${current_theme}=    Get Current Theme
```

**Parâmetros:**
- `theme` (string): O tema desejado ('light' ou 'dark')

**Retorno:**
- Booleano indicando sucesso da operação

### TerminateApplication

Extensão avançada da AppiumLibrary que permite encerrar aplicações Android durante a execução de testes automatizados. Esta keyword utiliza comandos ADB para garantir o encerramento completo do aplicativo, liberando recursos do sistema e permitindo testes de reinicialização. Também fornece funcionalidade para recuperar o ID do pacote do aplicativo atual sem necessidade de hardcoding.

**Principais funcionalidades:**
- Encerrar programaticamente uma aplicação Android durante a execução do teste
- Recuperar o identificador do aplicativo atual (`appPackage`) sem hardcoding
- Verificar se o aplicativo foi encerrado corretamente
- Testar cenários de reinicialização e recuperação de estado
- Simular comportamento de usuário fechando e reabrindo o aplicativo

**Compatibilidade:**
- Android 7.0 (Nougat) ou superior
- Requer permissões de depuração USB ativas

**Exemplo de uso:**
```robot
# Encerrar aplicativo específico
Terminate Application    com.example.myapp

# Encerrar o aplicativo atual em teste
${current_package}=    Get Current Application Package
Terminate Application    ${current_package}

# Encerrar e reiniciar aplicativo
Terminate Application    com.example.myapp
Sleep    2s    # Aguardar encerramento completo
Open Application    ${REMOTE_URL}    platformName=Android    appPackage=com.example.myapp    appActivity=.MainActivity
```

**Parâmetros:**
- `app_package` (string): O identificador do pacote Android a ser encerrado

**Retorno:**
- Booleano indicando sucesso da operação

**Implementação técnica:**
- Utiliza comandos ADB (`adb shell am force-stop`) para garantir encerramento completo
- Verifica processos ativos para confirmar encerramento
- Implementa mecanismo de retry para casos de aplicativos resistentes ao encerramento

### ClickElementV2

Keyword avançada que realiza cliques precisos em elementos durante testes com Appium e Robot Framework, usando a API W3C Actions para controlar a posição exata do toque na tela. Oferece flexibilidade no posicionamento do clique, permitindo definir offsets absolutos (em pixels) ou relativos (como porcentagem do tamanho do elemento), resolvendo problemas comuns de precisão em interações com elementos de UI em dispositivos Android.

**Principais funcionalidades:**
- Realizar cliques pixel-perfect em elementos, controlando o ponto exato dentro da área do elemento
- Permitir o uso de offsets relativos (% do tamanho do elemento) ou absolutos (px)
- Garantir que o clique seja executado dentro dos limites da tela
- Resolver problemas de elementos parcialmente visíveis ou sobrepostos
- Melhorar a estabilidade de testes em diferentes tamanhos de tela e densidades de pixel

**Compatibilidade:**
- Android 7.0 (Nougat) ou superior
- Implementação otimizada para Android 9+ com suporte completo a W3C Actions API

**Exemplo de uso:**
```robot
# Clicar no centro do elemento (comportamento padrão)
ClickC    id=com.app.example:id/botao_confirmar

# Clicar em uma posição específica dentro do elemento (50% da largura, 50% da altura)
ClickC    id=com.app.example:id/botao_confirmar    0.5    0.5

# Clicar em uma posição específica com offset absoluto em pixels
ClickC    id=com.app.example:id/botao_confirmar    x_offset=10    y_offset=15    use_absolute=True

# Clicar no canto superior esquerdo do elemento
ClickC    id=com.app.example:id/botao_confirmar    0.0    0.0
```

**Parâmetros:**
- `locator` (string): Localizador do elemento (id, xpath, accessibility_id, etc.)
- `x_offset` (float, opcional): Offset horizontal (0.0-1.0 para relativo, pixels para absoluto)
- `y_offset` (float, opcional): Offset vertical (0.0-1.0 para relativo, pixels para absoluto)
- `use_absolute` (boolean, opcional): Define se os offsets são absolutos (True) ou relativos (False)

**Implementação técnica:**
- Utiliza W3C Actions API para interações precisas com a tela
- Calcula coordenadas exatas baseadas no tamanho e posição do elemento
- Implementa validações de limites para garantir que o clique ocorra dentro da área visível
- Suporta todos os tipos de localizadores compatíveis com Appium

### Click Elements

Keyword personalizada projetada para realizar cliques sequenciais em múltiplos elementos em aplicações móveis usando Appium e Robot Framework. Fornece controle preciso sobre o tempo, duração e intervalos entre cliques.

**Principais funcionalidades:**
- Executar cliques sequenciais em múltiplos elementos de UI com tempo configurável
- Fornecer uma solução independente de dispositivo que funciona em diferentes aplicações Android
- Permitir sequências de interação automatizadas para fluxos de trabalho complexos

**Exemplo de uso:**
```robot
@{elements}=    Create List    id=button1    xpath=//android.widget.TextView[@text="Submit"]
Click Elements    ${elements}    click_duration=200    interval_between_clicks=0.5
```

### Compare Images

Keywords personalizadas projetadas para capturar e comparar screenshots durante testes automatizados com Appium e Robot Framework. Utilizam OpenCV e SSIM (Structural Similarity Index) para detectar diferenças visuais entre uma imagem de referência e a tela atual do aplicativo.

**Principais funcionalidades:**
- Capturar um screenshot de base para comparação posterior
- Comparar a tela atual com uma imagem de referência para detectar mudanças na UI
- Quantificar diferenças usando a métrica SSIM
- Gerar automaticamente uma imagem de diferença visual destacando as mudanças

**Exemplo de uso:**
```robot
Capture Initial Screenshot As    baseline.png
# Realizar alguma ação na UI...
Compare Final Screenshot With    screenshots/baseline.png    tolerance=0.02
```

### Get Network Connection Status

Keyword personalizada projetada para simplificar e padronizar a detecção de status de rede em dispositivos Android durante testes usando Appium e Robot Framework. Utiliza a propriedade `driver.network_connection` para interpretar o status de rede do dispositivo e retornar um resultado legível e significativo.

**Principais funcionalidades:**
- Interpretar claramente e confiavelmente o status de rede usando os valores de `bitmasks` do Appium
- Retornar uma string legível para o tipo de rede atual (Wi-Fi, dados móveis, modo avião ou sem conexão)
- Validar que o dispositivo está online antes de executar testes que requerem conectividade

**Exemplo de uso:**
```robot
${status}=    Get Network Connection Status
Log    ${status}    # Retorna: WIFI_ONLY, DATA_ONLY, WIFI_AND_DATA, AIRPLANE_MODE, NONE ou UNKNOWN
```

### Get Visible Elements On Screen

Keyword personalizada para recuperar elementos de UI visíveis na tela, com opções de filtragem por tipo e modo de depuração opcional. Projetada para automação de testes móveis com Robot Framework.

**Principais funcionalidades:**
- Fornecer um método confiável para capturar elementos de UI visíveis e válidos durante testes móveis baseados em Appium
- Filtrar resultados com base em tipos comuns de elementos e excluir referências não visíveis ou inválidas

**Exemplo de uso:**
```robot
${result}=    Get Visible Elements On Screen    clickable
Log    ${result}
```

### Long Press V2

Keyword personalizada projetada para realizar o gesto de pressionar e segurar em elementos em aplicativos Android ou iOS durante testes automatizados com Appium e Robot Framework. Utiliza o ActionChains do Selenium WebDriver para simular o pressionamento e manutenção de um elemento por uma duração especificada.

**Principais funcionalidades:**
- Facilitar ações de pressionar e segurar sem escrever código repetitivo nos casos de teste
- Controlar com precisão a duração do pressionamento
- Suportar qualquer estratégia de localização compatível com WebDriver

**Exemplo de uso:**
```robot
LongP    id=com.app.example:id/menu_button    2000
```

### Pinch

Keyword avançada projetada para simular um gesto realista de pinça (zoom out) em dispositivos Android durante testes usando Appium e Robot Framework. Esta implementação utiliza a API W3C Pointer Actions para criar gestos multi-touch precisos e configuráveis. Suporta tanto pinçamento direcionado a elementos específicos quanto gestos em tela cheia, com parâmetros ajustáveis para escala, duração, direção e outros aspectos do movimento.

**Principais funcionalidades:**
- Realizar gestos realistas de pinça (zoom out) multi-touch em testes automatizados de UI móvel
- Suportar direções de pinça vertical e horizontal
- Permitir pinçamento em elementos específicos ou no centro da tela quando nenhum localizador é fornecido
- Controlar precisamente a escala, velocidade e duração do gesto
- Simular gestos humanos com aceleração e desaceleração natural
- Validar limites da tela para evitar gestos inválidos
- Gerar logs detalhados para depuração de interações complexas

**Compatibilidade:**
- Android 7.0 (Nougat) ou superior
- Funcionalidade completa em Android 9+ com suporte a W3C Pointer Actions
- Otimizado para aplicações que utilizam gestos multi-touch (mapas, visualizadores de imagem, etc.)

**Exemplo de uso:**
```robot
# Pinça básica em um elemento específico (zoom out)
Perform Pinch Gesture    locator=id=map_view    scale=0.6

# Pinça vertical com duração personalizada
Perform Pinch Gesture    locator=id=map_view    scale=0.6    duration=800    direction=vertical

# Pinça horizontal com configurações avançadas
Perform Pinch Gesture    locator=id=image_viewer    scale=0.5    duration=1000    direction=horizontal    steps=15    pause_before=200    pause_after=300

# Pinça na tela inteira (sem localizador específico)
Perform Pinch Gesture    scale=0.7    duration=500
```

**Parâmetros:**
- `locator` (string, opcional): Localizador do elemento alvo (id, xpath, accessibility_id, etc.)
- `scale` (float): Fator de escala do gesto (0.1-0.9, onde valores menores = zoom out mais intenso)
- `duration` (int, opcional): Duração do gesto em milissegundos (padrão: 500ms)
- `direction` (string, opcional): Direção do gesto ('horizontal' ou 'vertical', padrão: 'horizontal')
- `steps` (int, opcional): Número de passos intermediários para simular movimento suave (padrão: 10)
- `pause_before` (int, opcional): Pausa antes do gesto em milissegundos (padrão: 0ms)
- `pause_after` (int, opcional): Pausa após o gesto em milissegundos (padrão: 0ms)

**Implementação técnica:**
- Utiliza W3C Pointer Actions API para gestos multi-touch precisos
- Calcula posições iniciais e finais dos dedos com base no elemento ou tela
- Implementa interpolação de movimento para simular gestos humanos naturais
- Valida parâmetros de entrada para evitar gestos impossíveis ou inválidos
- Gera logs detalhados para facilitar a depuração de problemas de interação

### Scroll

Biblioteca personalizada para Robot Framework e Appium, projetada para executar gestos de scroll/swipe dentro de elementos específicos de UI de aplicações móveis. Fornece controle preciso sobre direção, distância e velocidade, garantindo interações confiáveis mesmo dentro de áreas internas de elementos complexos.

**Principais funcionalidades:**
- Localização de elementos via diferentes estratégias (id, xpath, accessibility_id, etc.)
- Controle de direção (up, down, left, right)
- Porcentagem de scroll dentro do elemento
- Ajuste de velocidade do gesto

**Exemplo de uso:**
```robot
Scroll Inside    xpath=//android.widget.ScrollView    direction=down
```

### Scroll To Element

Keyword que fornece uma maneira robusta e configurável de rolar vertical ou horizontalmente até que um elemento específico se torne visível na tela. É projetada para trabalhar com AppiumLibrary no Robot Framework, suportando gestos de rolagem em tela cheia e baseados em contêiner.

**Principais funcionalidades:**
- Rolar verticalmente ou horizontalmente (up, down, left, right)
- Opcionalmente rolar dentro de um elemento de contêiner específico
- Detecção de visibilidade para parar a rolagem quando o elemento aparecer

**Exemplo de uso:**
```robot
Scroll To Element    id=login-button
```

### Swipe

Biblioteca personalizada para Robot Framework e Appium, projetada para realizar ações de swipe (gesto de arrastar) em elementos dentro da UI de aplicações móveis. Desenvolvida para fornecer maior controle sobre a direção do gesto, distância e velocidade, evitando interações imprecisas próximas às bordas dos elementos.

**Principais funcionalidades:**
- Localizar elementos via diferentes estratégias (id, xpath, accessibility_id, etc.)
- Definir a direção (up, down, left, right)
- Controlar a porcentagem de deslocamento (incluindo valores maiores que 100%)
- Ajustar a velocidade do gesto

**Exemplo de uso:**
```robot
Swipe Element    xpath=//android.widget.TextView[@text="Example"]    direction=right    percent=0.8    speed=500
```

### Tap At Percentage

Keyword personalizada projetada para simplificar e padronizar a funcionalidade de toque na tela em dispositivos Android durante testes usando Appium e Robot Framework. Utiliza coordenadas baseadas em porcentagem para tocar em pontos específicos da tela, tornando os testes mais confiáveis em diferentes tamanhos de tela.

**Principais funcionalidades:**
- Tocar em pontos específicos da tela usando coordenadas percentuais (0.0 a 1.0)
- Fornecer uma solução independente de dispositivo que funciona em diferentes tamanhos de tela
- Permitir interação precisa com elementos de UI quando localizadores tradicionais não estão disponíveis

**Exemplo de uso:**
```robot
Tap At Percentage    x=0.5    y=0.5    duration=200
```

### Wait Multiple Elements

Keyword personalizada projetada para esperar por múltiplos elementos simultaneamente em aplicações móveis usando Appium e Robot Framework. Fornece estratégias de espera flexíveis e retorna status detalhado de visibilidade para cada elemento.

**Principais funcionalidades:**
- Esperar por múltiplos elementos de UI se tornarem visíveis com estratégias configuráveis (ALL ou ANY)
- Fornecer uma solução independente de dispositivo que funciona em diferentes aplicações Android
- Permitir sincronização precisa para cenários de UI complexos quando múltiplos elementos carregam de forma assíncrona

**Exemplo de uso:**
```robot
@{locators}=    Create List    id=button1    xpath=//android.widget.TextView[@text="Submit"]
${result}=    Wait Multiple Elements    ${locators}    timeout=15    wait_for_all=True
```

### Zoom

Keyword avançada projetada para simular um gesto realista de pinça para fora (zoom in) em dispositivos Android durante testes usando Appium e Robot Framework. Esta implementação utiliza a API W3C Pointer Actions para criar gestos multi-touch precisos e configuráveis. Suporta tanto zoom direcionado a elementos específicos quanto gestos em tela cheia, com parâmetros ajustáveis para escala, duração, direção e outros aspectos do movimento.

**Principais funcionalidades:**
- Realizar gestos realistas de zoom multi-touch em testes automatizados de UI móvel
- Suportar direções de zoom vertical e horizontal
- Permitir zoom em elementos específicos ou no centro da tela quando nenhum localizador é fornecido
- Controlar precisamente a escala, velocidade e duração do gesto
- Simular gestos humanos com aceleração e desaceleração natural
- Validar limites da tela para evitar gestos inválidos
- Gerar logs detalhados para depuração de interações complexas

**Compatibilidade:**
- Android 7.0 (Nougat) ou superior
- Funcionalidade completa em Android 9+ com suporte a W3C Pointer Actions
- Otimizado para aplicações que utilizam gestos multi-touch (mapas, visualizadores de imagem, etc.)

**Exemplo de uso:**
```robot
# Zoom básico em um elemento específico
Perform Zoom Gesture    locator=id=map_view    scale=2.0

# Zoom vertical com duração personalizada
Perform Zoom Gesture    locator=id=map_view    scale=2.0    duration=800    direction=vertical

# Zoom horizontal com configurações avançadas
Perform Zoom Gesture    locator=id=image_viewer    scale=3.0    duration=1000    direction=horizontal    steps=15    pause_before=200    pause_after=300

# Zoom na tela inteira (sem localizador específico)
Perform Zoom Gesture    scale=1.5    duration=500
```

**Parâmetros:**
- `locator` (string, opcional): Localizador do elemento alvo (id, xpath, accessibility_id, etc.)
- `scale` (float): Fator de escala do gesto (1.1-5.0, onde valores maiores = zoom in mais intenso)
- `duration` (int, opcional): Duração do gesto em milissegundos (padrão: 500ms)
- `direction` (string, opcional): Direção do gesto ('horizontal' ou 'vertical', padrão: 'horizontal')
- `steps` (int, opcional): Número de passos intermediários para simular movimento suave (padrão: 10)
- `pause_before` (int, opcional): Pausa antes do gesto em milissegundos (padrão: 0ms)
- `pause_after` (int, opcional): Pausa após o gesto em milissegundos (padrão: 0ms)

**Implementação técnica:**
- Utiliza W3C Pointer Actions API para gestos multi-touch precisos
- Calcula posições iniciais e finais dos dedos com base no elemento ou tela
- Implementa interpolação de movimento para simular gestos humanos naturais
- Valida parâmetros de entrada para evitar gestos impossíveis ou inválidos
- Gera logs detalhados para facilitar a depuração de problemas de interação

**Diferenças em relação à keyword Pinch:**
- Direção oposta do movimento dos dedos (afastamento vs. aproximação)
- Valores de escala diferentes (>1.0 para zoom, <1.0 para pinch)
- Otimizações específicas para o comportamento de ampliação

## Compatibilidade e Limitações

### Versões do Android Suportadas

| Versão Android | Nome | Nível de API | Compatibilidade |
|----------------|------|-------------|----------------|
| Android 7.0-7.1 | Nougat | 24-25 | Básica |
| Android 8.0-8.1 | Oreo | 26-27 | Boa |
| Android 9 | Pie | 28 | Muito Boa |
| Android 10 | Q | 29 | Excelente |
| Android 11 | R | 30 | Excelente |
| Android 12 | S | 31-32 | Excelente |
| Android 13 | Tiramisu | 33 | Excelente |
| Android 14 | Upside Down Cake | 34 | Excelente |

### Matriz de Compatibilidade por Keyword

| Keyword | Android 7.0-7.1 | Android 8.0-8.1 | Android 9+ | Observações |
|---------|----------------|-----------------|------------|-------------|
| ChangeTheme | ⚠️ Limitado | ✅ Funcional | ✅ Completo | Funcionalidade completa em Android 10+ com suporte nativo a tema escuro |
| TerminateApplication | ✅ Funcional | ✅ Funcional | ✅ Completo | Requer permissões de depuração USB ativas |
| ClickElementV2 | ⚠️ Limitado | ✅ Funcional | ✅ Completo | Implementação otimizada para Android 9+ com suporte completo a W3C Actions API |
| Click Elements | ✅ Funcional | ✅ Funcional | ✅ Completo | Funciona em todas as versões suportadas |
| Compare Images | ✅ Funcional | ✅ Funcional | ✅ Completo | Pode ter variações de desempenho dependendo da resolução da tela |
| Get Network Connection Status | ✅ Funcional | ✅ Funcional | ✅ Completo | Funciona em todas as versões suportadas |
| Get Visible Elements On Screen | ✅ Funcional | ✅ Funcional | ✅ Completo | Funciona em todas as versões suportadas |
| Long Press V2 | ⚠️ Limitado | ✅ Funcional | ✅ Completo | Melhor precisão em Android 9+ |
| Pinch | ⚠️ Limitado | ⚠️ Limitado | ✅ Completo | Funcionalidade completa em Android 9+ com suporte a W3C Pointer Actions |
| Scroll | ✅ Funcional | ✅ Funcional | ✅ Completo | Funciona em todas as versões suportadas |
| Scroll To Element | ✅ Funcional | ✅ Funcional | ✅ Completo | Funciona em todas as versões suportadas |
| Swipe | ✅ Funcional | ✅ Funcional | ✅ Completo | Funciona em todas as versões suportadas |
| Tap At Percentage | ✅ Funcional | ✅ Funcional | ✅ Completo | Funciona em todas as versões suportadas |
| Wait Multiple Elements | ✅ Funcional | ✅ Funcional | ✅ Completo | Funciona em todas as versões suportadas |
| Zoom | ⚠️ Limitado | ⚠️ Limitado | ✅ Completo | Funcionalidade completa em Android 9+ com suporte a W3C Pointer Actions |

**Legenda:**
- ✅ Completo: Funcionalidade completa e otimizada
- ✅ Funcional: Funciona corretamente com possíveis limitações menores
- ⚠️ Limitado: Funcionalidade básica disponível, mas com limitações significativas

### Limitações Conhecidas

1. **Gestos Multi-touch Complexos**:
   - Alguns gestos muito complexos (como rotação com três dedos) podem não funcionar consistentemente em todos os dispositivos.
   - Dispositivos com Android 7.0 podem ter limitações na precisão de gestos multi-touch.

2. **Elementos Dinâmicos**:
   - Elementos que mudam rapidamente de posição ou tamanho durante a interação podem causar falhas nos gestos.
   - Recomenda-se adicionar esperas apropriadas antes de interagir com elementos dinâmicos.

3. **Fragmentação de Dispositivos**:
   - Devido à fragmentação do ecossistema Android, algumas keywords podem se comportar ligeiramente diferente em fabricantes específicos (Samsung, Xiaomi, etc.).
   - Recomenda-se testar em múltiplos dispositivos para garantir compatibilidade.

4. **Modo de Economia de Energia**:
   - Dispositivos em modo de economia de energia podem ter comportamento inconsistente com gestos complexos.
   - Recomenda-se desativar o modo de economia de energia durante os testes.

## Melhores Práticas

### Estratégias para Testes Robustos com Android

#### Estrutura de Testes

1. **Organize por Funcionalidade**: Estruture seus testes por funcionalidade do aplicativo, não por keywords.
   ```robot
   # Exemplo de organização por funcionalidade
   *** Test Cases ***
   Login Válido
       Abrir Aplicativo
       Preencher Credenciais    ${USUARIO_VALIDO}    ${SENHA_VALIDA}
       Verificar Login Com Sucesso
   ```

2. **Utilize Tags**: Adicione tags para categorizar testes e permitir execuções seletivas.
   ```robot
   *** Test Cases ***
   [Tags]    login    smoke    critical
   Login Válido
       # Passos do teste
   ```

3. **Implemente Retentativas**: Configure retentativas para testes instáveis em ambientes Android.
   ```robot
   *** Settings ***
   Test Timeout    2 minutes
   Test Retry Timeout    1 minute
   Test Retry Interval    5 seconds
   ```

#### Interação com Elementos

1. **Prefira IDs Estáveis**: Sempre que possível, use resource-ids ou accessibility-ids em vez de XPath.
   ```robot
   # Preferível
   ClickC    id=com.example.app:id/login_button
   
   # Evite quando possível
   ClickC    xpath=//android.widget.Button[@text="Login"]
   ```

2. **Implemente Esperas Inteligentes**: Use esperas explícitas em vez de sleeps fixos.
   ```robot
   # Bom
   Wait Multiple Elements    ${LOGIN_SCREEN_ELEMENTS}    timeout=15
   
   # Evite
   Sleep    5s    # Não recomendado
   ```

3. **Gestos Graduais**: Para gestos complexos (Pinch/Zoom), comece com valores conservadores.
   ```robot
   # Comece com gestos mais lentos e suaves
   Perform Zoom Gesture    locator=id=map_view    scale=1.5    duration=800    steps=15
   ```

#### Gerenciamento de Dispositivos

1. **Limpe o Estado**: Sempre limpe o estado do aplicativo entre testes.
   ```robot
   *** Keywords ***
   Reset App State
       Terminate Application    ${APP_PACKAGE}
       Sleep    1s
       Open Application    ${APPIUM_SERVER}    platformName=Android    appPackage=${APP_PACKAGE}    appActivity=${APP_ACTIVITY}
   ```

2. **Verifique Conectividade**: Valide o estado da rede antes de testes que dependem de conexão.
   ```robot
   *** Keywords ***
   Ensure Network Connection
       ${status}=    Get Network Connection Status
       Run Keyword If    '${status}' == 'NONE'    Fail    Dispositivo sem conexão de rede
   ```

3. **Capture Screenshots Estratégicos**: Capture screenshots em pontos críticos para depuração.
   ```robot
   *** Keywords ***
   Verify Screen After Login
       Capture Page Screenshot    login_result.png
       Compare Images    ${EXPECTED_LOGIN_SCREEN}    login_result.png    tolerance=0.05
   ```

## Exemplos de Casos de Teste

A seguir, apresentamos exemplos completos de casos de teste que demonstram como combinar as keywords deste repositório para criar testes robustos para aplicativos Android.

### Exemplo 1: Teste de Login com Validação Visual

```robot
*** Settings ***
Library           AppiumLibrary
Resource          ../resources/keywords.robot
Suite Setup       Open Test Application
Suite Teardown    Close Application
Test Teardown     Reset App State

*** Variables ***
${APPIUM_SERVER}    http://localhost:4723/wd/hub
${APP_PACKAGE}      com.example.loginapp
${APP_ACTIVITY}     .MainActivity
${VALID_USER}       usuario_teste
${VALID_PASSWORD}   senha123
${LOGIN_BUTTON}     id=com.example.loginapp:id/login_button
${USERNAME_FIELD}   id=com.example.loginapp:id/username_input
${PASSWORD_FIELD}   id=com.example.loginapp:id/password_input
${SUCCESS_MESSAGE}  id=com.example.loginapp:id/success_message

*** Test Cases ***
Login Com Credenciais Válidas
    [Tags]    login    smoke    critical
    # Verificar conectividade antes do teste
    ${network}=    Get Network Connection Status
    Run Keyword If    '${network}' == 'NONE'    Fail    Dispositivo sem conexão
    
    # Preencher formulário de login
    Wait Multiple Elements    ${USERNAME_FIELD},${PASSWORD_FIELD},${LOGIN_BUTTON}    timeout=10
    ClickC    ${USERNAME_FIELD}
    Input Text    ${USERNAME_FIELD}    ${VALID_USER}
    ClickC    ${PASSWORD_FIELD}
    Input Text    ${PASSWORD_FIELD}    ${VALID_PASSWORD}
    
    # Capturar screenshot antes do login
    Capture Page Screenshot    before_login.png
    
    # Executar login
    ClickC    ${LOGIN_BUTTON}
    
    # Verificar resultado com espera explícita
    Wait Until Element Is Visible    ${SUCCESS_MESSAGE}    timeout=15
    Element Should Contain Text    ${SUCCESS_MESSAGE}    Login realizado com sucesso
    
    # Validação visual da tela pós-login
    Capture Page Screenshot    after_login.png
    Compare Images    ${EXPECTED_LOGIN_SUCCESS}    after_login.png    tolerance=0.05

*** Keywords ***
Open Test Application
    Open Application    ${APPIUM_SERVER}
    ...    platformName=Android
    ...    appPackage=${APP_PACKAGE}
    ...    appActivity=${APP_ACTIVITY}
    ...    automationName=UiAutomator2

Reset App State
    Terminate Application    ${APP_PACKAGE}
    Sleep    1s
    Open Test Application
```

### Exemplo 2: Teste de Navegação em Mapa com Gestos Multi-touch

```robot
*** Settings ***
Library           AppiumLibrary
Resource          ../resources/keywords.robot
Suite Setup       Open Map Application
Suite Teardown    Close Application
Test Teardown     Reset Map State

*** Variables ***
${APPIUM_SERVER}    http://localhost:4723/wd/hub
${MAP_PACKAGE}      com.example.mapapp
${MAP_ACTIVITY}     .MapActivity
${MAP_VIEW}         id=com.example.mapapp:id/map_container
${SEARCH_BUTTON}    id=com.example.mapapp:id/search_button
${LOCATION_MARKER}  id=com.example.mapapp:id/location_pin

*** Test Cases ***
Navegar No Mapa Com Gestos Multi-touch
    [Tags]    map    gestures
    # Esperar carregamento do mapa
    Wait Until Element Is Visible    ${MAP_VIEW}    timeout=20
    Sleep    2s    # Aguardar estabilização do mapa
    
    # Realizar zoom in no mapa
    Perform Zoom Gesture    locator=${MAP_VIEW}    scale=2.0    duration=800    steps=15
    Sleep    1s
    
    # Realizar swipe para navegar no mapa
    Swipe Element    ${MAP_VIEW}    direction=left    percent=0.5    speed=500
    Sleep    1s
    Swipe Element    ${MAP_VIEW}    direction=up    percent=0.5    speed=500
    Sleep    1s
    
    # Realizar pinch para zoom out
    Perform Pinch Gesture    locator=${MAP_VIEW}    scale=0.5    duration=800    steps=15
    Sleep    1s
    
    # Verificar se o marcador de localização está visível
    ${elements}=    Get Visible Elements On Screen    clickable
    Should Contain    ${elements}    ${LOCATION_MARKER}
    
    # Clicar no marcador de localização
    ClickC    ${LOCATION_MARKER}
    
    # Verificar se o painel de informações aparece
    Wait Until Page Contains Element    id=com.example.mapapp:id/info_panel    timeout=10

*** Keywords ***
Open Map Application
    Open Application    ${APPIUM_SERVER}
    ...    platformName=Android
    ...    appPackage=${MAP_PACKAGE}
    ...    appActivity=${MAP_ACTIVITY}
    ...    automationName=UiAutomator2

Reset Map State
    # Resetar o estado do mapa para o padrão
    ${reset_button_exists}=    Run Keyword And Return Status    Page Should Contain Element    id=com.example.mapapp:id/reset_view_button
    Run Keyword If    ${reset_button_exists}    ClickC    id=com.example.mapapp:id/reset_view_button
    ...    ELSE    Terminate Application    ${MAP_PACKAGE}
```

## Como Contribuir

Contribuições são bem-vindas! Por favor, consulte o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para obter detalhes sobre como contribuir para este projeto.

### Processo de Contribuição

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-keyword`)
3. Implemente sua keyword seguindo o padrão de organização do projeto
4. Adicione testes adequados para sua implementação
5. Atualize a documentação, incluindo o README.md
6. Envie um Pull Request

## Licença

Este projeto está licenciado sob a licença Apache-2.0 - consulte o arquivo [LICENSE](LICENSE) para obter detalhes. Esta licença foi escolhida para manter compatibilidade com o ecossistema Robot Framework e Appium.

## Troubleshooting

### Problemas Comuns e Soluções

#### 1. Falhas na Conexão com o Dispositivo

**Problema**: O Appium não consegue se conectar ao dispositivo Android.

**Soluções**:
- Verifique se o dispositivo está conectado e com depuração USB ativada
- Execute `adb devices` para confirmar que o dispositivo é reconhecido
- Reinicie o servidor ADB: `adb kill-server && adb start-server`
- Verifique se as capabilities do Appium estão corretas (platformName, deviceName, etc.)

#### 2. Elementos Não Encontrados

**Problema**: Keywords falham ao localizar elementos na tela.

**Soluções**:
- Use o Appium Inspector para verificar os localizadores corretos
- Adicione esperas explícitas antes de interagir com elementos
- Verifique se o elemento está realmente visível na tela (pode ser necessário scroll)
- Tente estratégias de localização alternativas (XPath, ID, accessibility ID)

#### 3. Gestos Multi-touch Inconsistentes

**Problema**: Keywords como Pinch e Zoom não funcionam consistentemente.

**Soluções**:
- Verifique a versão do Android (recomendado Android 9+)
- Aumente o valor do parâmetro `duration` para gestos mais lentos e estáveis
- Aumente o valor do parâmetro `steps` para movimentos mais suaves
- Adicione pausas antes e depois dos gestos (`pause_before` e `pause_after`)

#### 4. Problemas de Desempenho

**Problema**: Testes executam lentamente ou com timeouts frequentes.

**Soluções**:
- Verifique a conexão USB (use um cabo de alta qualidade)
- Desative animações no dispositivo Android (nas opções de desenvolvedor)
- Aumente os valores de timeout nas configurações do Appium
- Feche aplicativos em segundo plano no dispositivo

#### 5. Erros de ADB

**Problema**: Comandos ADB falham ou retornam erros.

**Soluções**:
- Verifique se o ADB está no PATH do sistema
- Reinicie o servidor ADB: `adb kill-server && adb start-server`
- Reconecte o dispositivo fisicamente
- Verifique permissões de acesso ao dispositivo

## 📄 Organização do Repositório

O fluxo de trabalho neste repositório segue uma estratégia simples e eficiente de branches, garantindo organização, colaboração e integridade do código.

### 🚀 Branches

- **main** → Contém a versão estável do projeto. Nenhum desenvolvimento direto deve ser feito nesta branch.
- **develop** → Branch de integração. Todas as tarefas concluídas serão integradas aqui antes de serem movidas para `main`.
- **feature/** → Branches individuais para cada tarefa/keyword. Cada desenvolvedor trabalhará exclusivamente em sua branch.

Exemplo de nomenclatura das branches:
- `feature/keyword-long-press`
- `feature/keyword-pinch`
- `feature/keyword-zoom`

## ✅ Fluxo de Trabalho

1. **Criar a branch da sua tarefa**
    ```bash
    git checkout develop
    git pull
    git checkout -b feature/keyword-nome-da-keyword
    ```

2. **Desenvolver sua tarefa**
    - Realize commits pequenos e frequentes.
    - Sempre adicione mensagens claras nos commits.

3. **Enviar sua branch para o repositório**
    ```bash
    git push -u origin feature/keyword-nome-da-keyword
    ```

4. **Abrir um Pull Request**
    - Ao concluir a tarefa, abra um **Pull Request (PR)** para a branch `develop`.
    - O PR será revisado antes do merge.

5. **Merge para develop**
    - Após aprovação, o PR será integrado na branch `develop`.

6. **Merge para main**
    - Quando todas as tarefas forem concluídas e testadas na branch `develop`, será feito o merge para `main` com uma nova release.
**Pegar o local exato do app pra abrir:** adb shell dumpsys window | findstr "mCurrentFocus mFocusedApp

> **Importante:** Antes de iniciar ou continuar uma tarefa, sempre atualize sua branch local para evitar conflitos:
```bash
git checkout develop
git pull
git checkout feature/keyword-nome-da-keyword
git merge develop
