## Controller Python Script "processo_avaliacao_action"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=
##
from StringIO import StringIO

def tabela(lista):
    out = []
    for trabalho, palestrante in lista:
        out.append("%s (%s)" % (trabalho, palestrante))
    return "\n".join(out)

def processa(tipo):
    path = '/pycon/2010/sobre-o-evento/inscricoes'
    vocab = context.portal_catalog(path=path, portal_type=tipo)
    votos = context.REQUEST.get(tipo, [])
    info = {}
    for item in vocab:
        info[item.UID] = [item.Title.strip(), item.getNome]
    results = []
    for voto in votos:
        results.append(info.get(voto))
    return results

email = context.REQUEST.get('email')
palestras = processa('Palestra')
treinamentos = processa('Treinamento')

# Gera o conteudo do arquivo juiz.py, que eh enviado como anexo do email
out = StringIO()
out.write('# -*- coding: utf-8 -*-\n\n')
out.write('# %s\n' % email)
out.write('\nTreinamentos = """\n')
out.write(tabela(treinamentos))
out.write('\n"""\n')
out.write('\nPalestras = """\n')
out.write(tabela(palestras))
out.write('\n"""\n')

# Gera o nome do arquivo do juiz, baseado na primeira parte do email
filename = "juiz_%s.py" % email.split('@')[0]

# Envia os emails
context.processo_avaliacao_email(context, email=email, filename=filename, conteudo=out.getvalue())
context.processo_avaliacao_feedback(context, email=email)  

# Prepara a mensagem de agradecimento
message = "Obrigado por participar do processo de avaliação das propostas da PythonBrasil[6]!"
context.plone_utils.addPortalMessage(message, 'info')

return state
