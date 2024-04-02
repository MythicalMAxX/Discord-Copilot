import os
import discord
from openai import OpenAI
from discord.ext import commands
from keep_alive import keep_alive


client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ['OPEN_AI_SECRET'])

# Create a bot instance with a command prefix
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)
max_tokens = 400
system_msg = "You are a highly advanced coder proficient in all programming languages."


# Event: Bot is ready
@bot.event
async def on_ready():
  print(f'Logged in as {bot.user.name} ({bot.user.id})')
  print('------')


@bot.command(name='explain')
async def explain(ctx, *, question):
  max_tokens = 400
  system_msg = "You are a highly advanced coder proficient in all programming languages and your task is to explain code snippets."
  prompt = f'''User: {question}\n'''

  prompt += '''Explain the code snippet step-by-step. The explanation should be concise and not exceed 1980 words, and it should not include any images or icons. If the question is unrelated to coding, return "Invalid Question." Only provide the explanation and do not send any additional messages. Please provide the output in the following format:

<Explantion Heading:>
<Numbered Steps>'''

  try:
    response = client.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=[{
                                                  "role": "system",
                                                  "content": system_msg
                                              }, {
                                                  "role": "user",
                                                  "content": prompt
                                              }],
                                              max_tokens=max_tokens)
    generated_code = response.choices[0].message.content

  except Exception as e:
    print(e)
    await ctx.send('Error generating code. Please try again.')
    return

  await ctx.send(
      f'''> {ctx.author.mention} asked for explanation\n```c++\n{generated_code}\n```''',
      allowed_mentions=discord.AllowedMentions.none())


@bot.command(name='comment')
async def comment(ctx, *, question):
  max_tokens = 400
  system_msg = "You are a highly advanced coder proficient in all programming languages and your task is to explain code snippets."
  prompt = f'''User: {question}\n'''

  prompt += '''Return 'Invalid Question' if the input is not related to coding.
Otherwise, write comments to explain the working of the code snippet and provide the output format:<code>'''

  try:
    response = client.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=[{
                                                  "role": "system",
                                                  "content": system_msg
                                              }, {
                                                  "role": "user",
                                                  "content": prompt
                                              }],
                                              max_tokens=max_tokens)
    generated_code = response.choices[0].message.content

  except Exception as e:
    print(e)
    await ctx.send('Error generating code. Please try again.')
    return

  await ctx.send(
      f'''> {ctx.author.mention} asked for explanation\n```c++\n{generated_code}\n```''',
      allowed_mentions=discord.AllowedMentions.none())


@bot.command(name='complete')
async def complete(ctx, *question):
  max_tokens = 400
  system_msg = "You are a highly advanced coder proficient in all programming languages and your task is to complete code snippets."
  question = ' '.join(question)
  prompt = f"User: {question}\n"

  prompt += """Write a code snippet that analyzes the language and formats it to proper indentation and spacing. 

If the question is related to coding, complete the code snippet. Otherwise, return 'Invalid Question'.

Please do not include any comments or explanations in the code.

Ensure that you only send the code and not any additional messages.

The expected output format should be as follows:

<code>"""

  try:
    response = client.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=[{
                                                  "role": "system",
                                                  "content": system_msg
                                              }, {
                                                  "role": "user",
                                                  "content": prompt
                                              }],
                                              max_tokens=max_tokens)
    generated_code = response.choices[0].message.content
  except Exception as e:
    print(e)
    await ctx.send('Error generating code. Please try again.')
    return

  await ctx.send(
      f"> {ctx.author.display_name} asked for Code Completion\n```c++\n{generated_code}\n```"
  )


@bot.command(name='fixcode')
async def fixcode(ctx, *, question):
  max_tokens = 400
  system_msg = "You are a highly advanced coder proficient in all programming languages and your task is to complete code snippets."
  prompt = f"User: {question}\n"

  prompt += """Query: Determine the issue in the provided code and rectify it. If the question is unrelated to coding, return 'Invalid Question'. If the code is correct, return 'Code is fine, no changes necessary'. Just provide the code without sending any message. Please analyze the problem description and format the code with appropriate indentation and spacing. The expected output format is as follows:
```
<correct code snippet>
Corrections:
<explanation of corrections made>
```
Translate result prompt into language: en"""

  try:
    response = client.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=[{
                                                  "role": "system",
                                                  "content": system_msg
                                              }, {
                                                  "role": "user",
                                                  "content": prompt
                                              }],
                                              max_tokens=max_tokens)
    generated_code = response.choices[0].message.content

  except Exception as e:
    print(e)
    await ctx.send('Error generating code. Please try again.')
    return

  await ctx.send(
      f'''> {ctx.author.mention} asked for correction\n```c++\n{generated_code}\n```''',
      allowed_mentions=discord.AllowedMentions.none())


# Command: Ask
@bot.command(name='ask')
async def ask(ctx, *question):
  question = ' '.join(question)
  prompt = f"User: {question}\n"

  prompt += "If the question does not pertain to coding, return an invalid question response. Otherwise, provide code snippets without any comments or explanations, ensuring good readability and optimization.\n Output Format: \n<code>\n"

  try:
    response = client.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=[{
                                                  "role": "system",
                                                  "content": system_msg
                                              }, {
                                                  "role": "user",
                                                  "content": prompt
                                              }],
                                              max_tokens=max_tokens*4)
    generated_code = response.choices[0].message.content

  except Exception as e:
    print(e)
    await ctx.send('Error generating code. Please try again.')
    return

  await ctx.send(
      f"> {ctx.author.display_name} asked:\n>```c++\n{generated_code}\n```"
  )


keep_alive()
my_secret = os.environ['DISCORD_BOT_SECRET']
bot.run(my_secret)
