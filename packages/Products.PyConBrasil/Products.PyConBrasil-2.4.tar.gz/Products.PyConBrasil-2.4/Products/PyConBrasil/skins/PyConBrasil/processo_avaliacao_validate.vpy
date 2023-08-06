## Controller Validator "processo_avaliacao_validate"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=Treinamento, Palestra, email
##title=
##
if not email:
   state.setError('email', 'É obrigatório informar o seu e-mail.')

if state.getErrors():
   state.setStatus('failure')

return state
