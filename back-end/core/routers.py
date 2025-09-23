class CoreRouter:
    """
    Um roteador para controlar todas as operações de banco de dados em aplicativos
    dentro do projeto core.
    """
    def db_for_read(self, model, **hints):
        """
        Tentativas de leitura dos modelos do core não devem ir para o banco de dados 'default'.
        """
        if model._meta.app_label == 'core':
            return None  # Indica para o Django não usar nenhum banco de dados configurado
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Tentativas de escrita dos modelos do core não devem ir para o banco de dados 'default'.
        """
        if model._meta.app_label == 'core':
            return None
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Permite relações se ambos os objetos estiverem no app 'core' ou ambos
        estiverem em apps que usam o banco de dados 'default'.
        """
        if obj1._meta.app_label == 'core' or \
           obj2._meta.app_label == 'core':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Certifica-se de que o app 'core' só apareça no banco de dados 'default'
        se não for o app 'core'.
        """
        if app_label == 'core':
            return False  # Nós gerenciamos os modelos do 'core' com MongoEngine, não com o Django ORM
        return True # Permite migrações para todos os outros apps
