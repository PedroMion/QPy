# 🇧🇷 pt-BR

## 📖 Sobre este projeto
Projeto de uma biblioteca Python para realização de **simulações de filas computacionais**. Dessa forma, o artefato provê uma interface simples para a configuração e execução de experimentos relacionados a teoria de filas, sejam estas abertas ou fechadas. 

Para os intervalos de **tempo de serviço**, **chegada** e de **pensamento**, as seguintes distribuições são disponibilizadas:
- Exponencial
- Constante
- Uniforme
- Normal

Já para as **disciplinas de atendimento** nos servidores, são cinco possibilidades:
- Primeiro a chegar, primeiro a sair (FCFS)
- Primeiro a chegar, último a sair (LCFS)
- Menor tempo restante (SRT), com ou sem preempção 
- Cíclico (Round Robin)
- Fila de prioridade

Além da biblioteca, uma API simples também foi desenvolvida, possibilitando a utilização do sistema por uma **aplicação web**.

## 📺 Tecnologias
- **Aplicação:** Python
- **API:** FastAPI
- **Bibliotecas:** Pydantic, NumPy
- **Deploy:** Em breve

## 📰 Modo de uso
Para utilizar a aplicação, importe a biblioteca. O primeiro passo a ser tomado é a instanciação do objeto da classe `Environment`. O ambiente é o responsável por controlar o estado da simulação.

```python
env = Environment()
```

Caso deseje um sistema fechado, o número de terminais e a distribuição do tempo de pensamento devem ser fornecidos.
Se apenas um deles não for informado, a rede será considerada aberta.

Para definir distribuições, utilize a classe estática `Distribution`, que segue o padrão factory. Ela fornece métodos que instanciam e retornam objetos prontos para uso, sem a necessidade de importar diretamente cada classe de distribuição.
Todas implementam a mesma interface abstrata, o que permite o uso genérico em qualquer parte do sistema.

```python
env = Environment(number_of_terminals=24, think_time_distribution=Distribution.constant(value=0))
```

Com o ambiente pronto, servidores podem ser adicionados. O método `add_server` recebe a distribuição de serviço e a disciplina de fila.
A disciplina segue o mesmo padrão factory da classe `QueueDiscipline`. O método retorna o ID do servidor, que será utilizado em outras configurações do ambiente.

```python
a = env.add_server(service_distribution=Distribution.constant(value=(2)), queue_discipline=QueueDiscipline.fcfs())
```

Para conectar dois servidores, utilize `add_servers_connection`, informando o ID do servidor de origem, o de destino e a probabilidade de roteamento.
Probabilidades de saída não especificadas serão interpretadas como saídas do sistema. Por exemplo, se 25% dos jobs saem do servidor A para o servidor B e mais nada é definido, os 75% restantes serão finalizados após o servidor A.

```python
env.add_servers_connection(origin_server_id=a, destination_server_id=b, routing_probability=0.25)
```

Para configurar pontos de chegada, há duas opções:
- Em redes abertas, adicione pontos de entrada com a distribuição de chegada e, opcionalmente, uma distribuição de prioridade.
- Em redes fechadas, configure as probabilidades de saída dos terminais, definindo os caminhos possíveis para novos jobs.

```python
env.add_entry_point(server_id=a, arrival_distribution=Distribution.constant(1), priority_distribution=None)
env.add_terminals_routing_probability(destination_server_id=a, routing_probability=1)
```

Após a configuração, chame o método `simulate`, informando o tempo total e o tempo de aquecimento da simulação.

```python
result = env.simulate(time_in_seconds=4000000, warmup_time=1000000)
```

Os resultados podem ser acessados individualmente, através dos métodos `get`, ou exibidos diretamente no console com o método `show_simulation_results`.


# 🇺🇸 en-US

## 📖 About this project
A Python library designed to **simulate computer queueing systems**.  
It provides a simple and flexible interface to configure and run experiments related to queueing theory, supporting both open and closed network models.  

For **service times**, **arrival times**, and **think times**, the following distributions are available:
- Exponential  
- Constant  
- Uniform  
- Normal  

For **server queue disciplines**, five options are supported:
- First Come, First Served (FCFS)  
- Last Come, First Served (LCFS)  
- Shortest Remaining Time (SRT), with or without preemption  
- Round Robin  
- Priority Queue  

In addition to the core library, a **simple API** has been developed, allowing the system to be used through a **web application**.

## 📺 Technologies
- **Application:** Python  
- **API:** FastAPI  
- **Libraries:** Pydantic, NumPy  
- **Deployment:** Coming soon  

## 📰 How to use
To use the library, import it and **create a simulation environment**.  
Start by instantiating the `Environment` class, which manages the simulation state and flow.

```python
env = Environment()
```

If you want a closed system, you must define both the number of terminals and the think time distribution.
If only one of them is omitted, the network will be considered open.

Distributions can be created using the static class `Distribution`, which follows the factory pattern.
It provides ready-to-use methods that instantiate and return distribution objects without requiring direct class imports.
All distributions share a common abstract interface, allowing for generic use throughout the system.

```python
a = env.add_server(service_distribution=Distribution.constant(value=(2)), queue_discipline=QueueDiscipline.fcfs())
```

Once the environment is ready, servers can be added using the `add_server` method.
It receives the service distribution and the queue discipline.
Queue disciplines follow the same factory approach, implemented by the `QueueDiscipline` class.
The method returns the server ID, which can be used for further configuration.

```python
a = env.add_server(service_distribution=Distribution.constant(value=2), queue_discipline=QueueDiscipline.fcfs())
```

To connect two servers, use `add_servers_connection`, passing the origin server ID, the destination server ID, and the routing probability.
Unspecified routing probabilities are interpreted as exit points from the system.
For example, if 25% of jobs go from server A to server B and no other routes are defined, the remaining 75% will leave the system after server A.

```python
env.add_servers_connection(origin_server_id=a, destination_server_id=b, routing_probability=0.25)
```

To configure arrival points, there are two options:
- In open networks, add entry points with an arrival distribution and, optionally, a priority distribution.
- In closed networks, configure terminal routing probabilities to define all possible paths for new jobs.

```python
env.add_entry_point(server_id=a, arrival_distribution=Distribution.constant(1), priority_distribution=None)
env.add_terminals_routing_probability(destination_server_id=a, routing_probability=1)
```

After the setup is complete, call `simulate` with the total simulation time and the warm-up period.

```python
result = env.simulate(time_in_seconds=4000000, warmup_time=1000000)
```

Simulation results can be accessed individually using the `get` methods or displayed in the console with `show_simulation_results`.
