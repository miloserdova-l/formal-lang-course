## Консольное приложения для работы с графовыми БД
Для того, чтобы узнать, какие доступны команды, следует выполнить команду:

```bash
python -m project -h
```

### Примеры использования:

```bash
python -m project simple -print-graph-info pizza
```

```bash
python -m project simple -gen-graph 10 15 x y ./output/graph.dot
```

```bash
python -m project rpq -regex ac -graph ./output/graph.dot -start-nodes 1 2 -final-nodes 3
```
