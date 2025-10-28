# Hand Tracking Project

## Objetivo
O objetivo deste projeto é implementar um sistema de rastreamento de mãos utilizando a biblioteca **MediaPipe**. O sistema é capaz de detectar mãos em tempo real, identificar a posição dos dedos e contar quantos dedos estão levantados. Este projeto pode ser utilizado como base para aplicações de interação gestual, como controle de interfaces ou jogos.

## Tema Relacionado
O projeto está relacionado ao tema de **Visão Computacional** e **Interação Humano-Computador (HCI)**. Ele utiliza técnicas de processamento de imagem e aprendizado de máquina para detectar e rastrear mãos em vídeos capturados por uma câmera.

## Status do Projeto
Este projeto ainda está em desenvolvimento e tem a intenção de se tornar um repositório de módulos para visão computacional, contendo diferentes projetos relacionados ao tema. O rastreamento de mãos é o primeiro módulo implementado, e novos módulos serão adicionados futuramente.

## Arquivos do Projeto
- **`HandTrackingModule.py`**: Contém a implementação da classe `HandDetector`, que encapsula as funcionalidades de detecção e rastreamento de mãos utilizando a biblioteca MediaPipe.
- **`CountFingers.py`**: Script principal que utiliza o `HandTrackingModule` para capturar vídeo em tempo real, detectar mãos e contar os dedos levantados. Exibe os resultados na tela.
- **`requirements.txt`**: Lista de dependências necessárias para executar o projeto, incluindo as versões específicas das bibliotecas.

## Requisitos de Versão do Python

O projeto utiliza a biblioteca *MediaPipe*, que é compatível com versões do Python entre *3.9 e 3.12*. A versão mais segura recomendada é o *Python 3.11*.


## Como Testar
### Dependências
Certifique-se de que as dependências listadas no arquivo `requirements.txt` estão instaladas. Para isso, execute o seguinte comando no terminal:

```bash
pip install -r [requirements.txt](http://_vscodecontentref_/0)
```

### Passos para testar:
    1 - Certifique-se de que sua câmera está conectada e funcionando.

    # Lembrando que HandTrackingModule.py é um módulo que é chamado por outra função!
    2 - Execute o script CountFingers.py (Por enquanto o único funcional):
        -> python CountFingers.py
        
    3 - A janela de vídeo será exibida, mostrando as mãos detectadas e o número de dedos levantados.


## Observação 

Se encontrar problemas com a detecção de mãos ou dedos, verifique se há boa iluminação e se a câmera está posicionada corretamente.

# Conclusão
Este projeto demonstra como utilizar a biblioteca MediaPipe para rastreamento de mãos e pode ser expandido para incluir funcionalidades adicionais, como reconhecimento de gestos ou controle de dispositivos. No futuro, ele será parte de um repositório maior, com múltiplos módulos para visão computacional.

