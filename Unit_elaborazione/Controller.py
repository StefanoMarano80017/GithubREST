from Broker import Broker
from Unit_elaborazione import Analisi_sorgente


# La classe controller ha il compito di coordinare le funzioni di analisi sui repository
class Controller:
    def __init__(self, token, db_file, logger):
        self.broker = None
        self.token = token
        self.db_file = db_file
        self.log = logger

    def get_git_data(self, query_string: str, size_max):
        # eseguo query su git e salvo i dati sul db
        self.broker = Broker.Broker(self.token, self.db_file, self.log)
        self.broker.do_search(query_string, size_max)
        self.broker = None

    def get_repo(self) -> list:
        # ottengo i dati dal db
        self.broker = Broker.Broker(self.token, self.db_file, self.log)
        repos = self.broker.get_repo()
        self.broker = None
        return repos

    def print_repo(self):
        self.broker = Broker.Broker(self.token, self.db_file, self.log)
        self.broker.print_table_repo()
        self.broker = None

    def get_link(self, id):
        self.broker = Broker.Broker(self.token, self.db_file, self.log)
        links = self.broker.get_link_repo(id)
        self.broker = None
        return links

    def repo_cloc(self) -> list:
        result_cloc = []
        self.broker = Broker.Broker(self.token, self.db_file, self.log)
        for repo in self.broker.get_repo():
            # La chiamata al broker ha lo scopo di leggere i dati presenti nel db
            links = self.broker.get_link_repo(repo[0])
            a = Analisi_sorgente.Analyzer(group=repo[1])
            # Viene effettuata l'analisi della repository e aggiunta alla lista
            cloc_result = a.cloc_files(links)
            self.log.write(cloc_result, 'f+g')
            result_cloc.append([cloc_result, repo[2], repo[3]])
            # print(result_cloc)
        self.broker = None
        return result_cloc

    def cloc_density_graph(self):
        list_raw = self.repo_cloc()
        li_r = []
        for li in list_raw:
            try:
                total_lines = li[0][0] + li[0][1] + li[0][2]
                density = (li[0][1] / total_lines) * 100
            except ZeroDivisionError:
                density = 0
            finally:
                li_f = [density, li[1], li[2]]
                li_r.append(li_f)
        return li_r

    def close(self):
        self.broker = Broker.Broker(self.token, self.db_file, self.log)
        self.broker.delete_db()
        self.broker = None

    def backup(self, backup_file):
        self.broker = Broker.Broker(self.token, self.db_file, self.log)
        self.broker.backup(backup_file)
        self.broker = None
