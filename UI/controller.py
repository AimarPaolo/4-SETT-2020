import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.choicefilm = None

    def handle_grafo(self, e):
        self._view.txt_result.controls.clear()
        rank = self._view.txt_rank.value
        if rank is None or rank == "":
            self._view.create_alert("Inserire il rank")
            self._view.update_page()
            return
        try:
            rank_int = float(rank)
        except ValueError:
            self._view.create_alert("Il rank inserito è una stringa")
            self._view.update_page()
            return
        if (0.0 < rank_int < 10.0) is False:
            self._view.create_alert("Rank inserito errato!!")
            self._view.update_page()
            return
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato!"))
        self._model.buildGraph(rank_int)
        nNodes, nEdges = self._model.getCaratteristiche()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo creato ha {nNodes} nodi"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo creato ha {nEdges} archi"))
        self.fillDD()
        self._view.update_page()

    def handle_massimo(self, e):
        nodo, grado = self._model.getGradoMax()
        self._view.txt_result.controls.append(ft.Text(f"Film grado MASSIMO:"))
        self._view.txt_result.controls.append(ft.Text(f"{nodo.id} - {nodo.name}({grado})"))
        self._view.update_page()

    def handle_cammino(self, e):
        self._view.txt_result.controls.clear()
        if self.choicefilm is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare un film!!"))
            self._view.update_page()
            return
        cammino_migliore, peso = self._model.getBestPath(self.choicefilm)


    def fillDD(self):
        for m in self._model._grafo.nodes:
            self._view.dd_film.options.append(ft.dropdown.Option(data=m, text=m.name, on_click=self.readData))

    def readData(self, e):
        if e.control.data is None:
            self.choicefilm = None
        else:
            self.choicefilm = e.control.data

