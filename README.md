# Asynchronous Task Queue Server

> This project provides an API accepting email post request and  
> deliver this email asynchronously

**Below desc from ChatGPT**

> Django Celery is a task queue library for Django web applications that allows you to run time-consuming tasks
> asynchronously in the background. It provides a way to schedule and execute long-running tasks outside the
> request-response cycle, so your web application can continue processing other requests without waiting for these tasks
> to complete.
> With Django Celery, you can create background tasks to perform tasks such as sending emails, processing images, or
> scraping data, and then call these tasks as needed from your Django views or models. The tasks are then executed by a
> separate process or group of processes, called workers, which run in the background. This allows you to take advantage
> of parallel processing and distribute the load across multiple processes.
> In summary, Django Celery is a powerful tool for running background tasks in Django applications and can greatly
> improve
> the performance and scalability of your application.

## Email Task Server Usage

1. **URL:** http://192.168.26.99:8080/email/

```json
{
  "from": "no-reply@waiwhanau.com",
  "to": "addr1@gmail.com,addr2@hotmail.com",
  "subject": "Test local celery 20481111",
  "text_content": "This is the test text content",
  "html_content": "<strong>Hello World</strong><br/>This is the test html content<br/>Thanks",
  "token": "ask admin",
  "callback": "https://url"
}
```

2. Fields Desc

| Fields       | Type   | Required | Desc                                                                                                                                                                                                              |
|--------------|--------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| from         | String | Y        | Fixed, don't change                                                                                                                                                                                               |
| to           | String | Y        | single or multiple address, note, user will see all recepants in email                                                                                                                                            |
| subject      | String | Y        |                                                                                                                                                                                                                   |
| text_content | String | N        | will use this as mail body, If the user's email system don't support html email                                                                                                                                   |
| html_content | String | Y        | use as email body when corresponding email system support html email                                                                                                                                              |
| token        | String | Y        | Keep it safe                                                                                                                                                                                                      |
| callback     | Number | N        | An url for task server to callback after email are sent. e.g. https://wms.server/send-email/callback/?checkout-id=12 <br>Then after email were sent you will get a notice and mark your model as "reminder sent". |

3. Restriction

Only allow requests from ['127', '192', '172', '10'].xxx.xxx.xxx.

