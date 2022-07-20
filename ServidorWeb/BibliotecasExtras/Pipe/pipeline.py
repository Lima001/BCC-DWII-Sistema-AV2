class Pipeline:

    def __init__(self):
        self.pipes = []
        self.args = []

    def add_pipe(self, function, arg):
        self.pipes.append(function)
        self.args.append(arg)

    def process(self):
        if len(self.pipes) == 0:
            print("Pipeline Vazio - Impossível de processar!")
            return

        for i in range(len(self.pipes)):
            if self.args[i] != (None,):
                self.pipes[i](*self.args[i])