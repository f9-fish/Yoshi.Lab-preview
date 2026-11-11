"""All remote traffic is intercepted: no live Firebase, studioApi or Gemini access."""
from pathlib import Path
from urllib.parse import urlparse
import json,mimetypes
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
types=['vocabulary','cloze','qa','trueFalse','discussion']
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in [390,1366]:
  ctx=browser.new_context(viewport={'width':width,'height':900});page=ctx.new_page();calls=[];errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  def route(r):
   u=urlparse(r.request.url)
   if u.hostname=='studioapi-bfaa4wjjga-an.a.run.app':
    calls.append(u.path);assert u.path=='/generate';assert r.request.headers['authorization']=='Bearer mock-token'
    if page.evaluate('window.__fail'):r.fulfill(status=429,json={'error':'利用回数の上限'});return
    r.fulfill(json={'questions':{t:[{'question':'Question '+t,'answer':'Answer','translation':'日本語'}] for t in types}});return
   if u.hostname!='local.test':r.abort();return
   if u.path.endswith('/preview-auth.js'):
    r.fulfill(content_type='text/javascript',body="""let listeners=[];window.YoshiAccount={user:null,subscribe(fn){listeners.push(fn);fn(this.user)},async login(){this.user={uid:'teacher-one'};listeners.forEach(fn=>fn(this.user))},async logout(){this.user=null;listeners.forEach(fn=>fn(null))},async isTeacher(){return !!this.user&&!window.__student},async getToken(){return 'mock-token'}};""");return
   path=root/u.path.split('/Yoshi.Lab-preview/')[-1]
   if not path.is_file():r.fulfill(status=404,body='not found');return
   r.fulfill(body=path.read_bytes(),content_type=mimetypes.guess_type(str(path))[0] or 'application/octet-stream')
  page.route('**/*',route)
  page.goto('https://local.test/Yoshi.Lab-preview/teacher-studio.html')
  assert page.locator('#editor').is_hidden();assert page.locator('#publish,#publishPanel').count()==0
  page.evaluate("document.getElementById('generate').click()")
  assert len(calls)==0
  page.locator('#login').click();page.locator('#editor').wait_for(state='visible')
  page.locator('#lesson').fill('test');page.locator('#source').fill('This is an original test passage.');page.locator('#count').fill('1')
  page.evaluate("document.getElementById('generate').click();document.getElementById('generate').click()")
  page.locator('.question').first.wait_for();assert len(calls)==1;assert page.locator('.category').count()==5
  page.locator('.question textarea').first.fill('Edited question');page.locator('.question input').first.uncheck();page.locator('#save').click()
  assert 'ブラウザ' in page.locator('#message').inner_text()
  page.reload();page.locator('#login').click();page.locator('#restore').click()
  page.locator('.question').first.wait_for();assert page.locator('.question textarea').first.input_value()=='Edited question';assert not page.locator('.question input').first.is_checked()
  page.screenshot(path=f'/tmp/studio-preview-{width}.png',full_page=True)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.evaluate('window.__fail=true');page.locator('#generate').click();page.wait_for_function("document.getElementById('message').textContent.includes('上限')")
  assert page.locator('#generate').is_enabled()
  page.locator('#logout').click();assert page.locator('#editor').is_hidden();assert page.locator('#review').is_hidden();assert page.locator('#source').input_value()==''
  page.evaluate('window.__student=true');page.locator('#login').click();page.wait_for_function("document.getElementById('authStatus').textContent==='教員権限がありません'")
  previous=len(calls);page.evaluate("document.getElementById('generate').click()");assert len(calls)==previous
  assert not errors,errors;ctx.close();print('PASS',width,'login gate, teacher gate, five types, duplicate submission, edit, local draft restore, error, logout, mobile layout; no publish or external access')
 browser.close()
