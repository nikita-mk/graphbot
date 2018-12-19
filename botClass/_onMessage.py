def on_message(self, event):
        # Ignore edits and uploads
        print('ting')
        print(event)
        subtype = event.get('subtype', '')
        print(subtype)
        if subtype == u'message_changed' or subtype == u'file_share' or subtype == u'bot_message':
            return

        # Don't respond to messages sent by the bot itself
        if event.get('user', '') == self.bot_id:
            return

        full_text = event.get('text', '') or ''

        # Only respond to messages addressed directly to the bot
#         if full_text.startswith(self.bot_id):
#             # Strip off the bot id and parse the rest of the message as the question
#         print(full_text)
        if event.get('bot_id','')=='':
            question = full_text
            if len(question) > 0:
                question = question.strip().lower()
                channel = event['channel']
                print(question)
                if question.find('list graph shortcuts')!=-1:
                    print('list')
                    self.respond(channel, f'I know about these graphs: {self.graph_shortcuts}')
                elif question.find('graph')!=-1:
                    print('graph')
                    self.respond(channel, 'Please wait...', [],True)
                elif question.find('kubectl')!=-1:
                    print('kubectl')
                    text = question.split(' ')
                    print(len(text))
                    self.respond(channel,'',text[1:],False,False,True)
                elif question.find('cpu')!=-1:
                    print('cpu')
                    self.respond(channel, 'Please wait...', [],False,True)
                elif question.find('help')!=-1:
                    print('help')
                    self.respond(channel, f'I can answer questions about: {self.help_msg}')
                else:
                    self.respond(channel, f'Sorry, I can only answer questions about: {self.help_msg}')
        