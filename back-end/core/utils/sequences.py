from core.documents import SequenceDocument

def get_next_sequence_value(sequence_name):
    """
    Busca o nome da sequência, incrementa o valor em 1 e o retorna.
    É atômico, o que previne que o mesmo número seja dado a duas chamadas simultâneas.
    """
    sequence = SequenceDocument.objects(name=sequence_name).modify(
        upsert=True,  # Cria o contador se ele não existir
        new=True,     # Retorna o documento modificado
        inc__sequence_value=1
    )
    return sequence.sequence_value