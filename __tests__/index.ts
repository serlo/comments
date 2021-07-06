import { MessageProviderPact, Verifier } from '@pact-foundation/pact'

import axios from 'axios'
import * as path from 'path'

const root = path.join(__dirname, '..')

test('HTTP Contract', async () => {
  await new Verifier({
    provider: 'Commenting System',
    providerBaseUrl: 'http://localhost:8000',
    stateHandlers: {
      'no threads exist': () => {
        return axios.post('http://localhost:8000/pact/set-state/', {
          consumer: 'serlo.org',
          state: 'no threads exist',
        })
      },
      'one thread for entity 234 exists': () => {
        return axios.post('http://localhost:8000/pact/set-state/', {
          consumer: 'serlo.org',
          state: 'one thread for entity 234 exists',
        })
      },
    },
    pactUrls: [
      path.join(root, 'pacts', 'http', 'serlo.org-commenting_system.json'),
    ],
  }).verifyProvider()
})

test('Message Contract', async () => {
  await new MessageProviderPact({
    messageProviders: {
      'a `create-thread` message': async () => {
        const message = {
          type: 'create-thread',
          payload: {
            author: {
              provider_id: 'serlo.org',
              user_id: '456',
            },
            entity: {
              provider_id: 'serlo.org',
              id: '123',
            },
            title: 'Title',
            content: 'Content',
            created_at: '2015-08-06T16:53:10+01:00',
            source: {
              provider_id: 'serlo.org',
              type: 'discussion/create',
            },
          },
        }
        await axios.post('http://localhost:8000/pact/execute-message/', message)
        return message
      },
      'a `create-comment` message': async () => {
        const { data } = await axios.get(
          'http://localhost:8000/threads/serlo.org/234/'
        )
        const message = {
          type: 'create-comment',
          payload: {
            author: {
              provider_id: 'serlo.org',
              user_id: '456',
            },
            thread_id: data[0].id,
            entity: {
              provider_id: 'serlo.org',
              id: '234',
            },
            content: 'Content',
            created_at: '2015-08-06T16:53:10+01:00',
            source: {
              provider_id: 'serlo.org',
              type: 'discussion/create',
            },
          },
        }
        await axios.post('http://localhost:8000/pact/execute-message/', message)
        return message
      },
    },
    provider: 'Commenting System',
    stateHandlers: {
      'no threads exist': () => {
        return axios.post('http://localhost:8000/pact/set-state/', {
          consumer: 'serlo.org',
          state: 'no threads exist',
        })
      },
      'one thread for entity 234 exists': () => {
        return axios.post('http://localhost:8000/pact/set-state/', {
          consumer: 'serlo.org',
          state: 'one thread for entity 234 exists',
        })
      },
    },
    pactUrls: [
      path.join(root, 'pacts', 'message', 'serlo.org-commenting_system.json'),
    ],
  }).verify()
})
