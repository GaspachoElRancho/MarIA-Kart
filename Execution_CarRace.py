# Mama mIA aka MarIA Kart
# Execution Car Race

# Luc Meunier - Thibault Dos Santos - Lilian De Conti - Jérôme Kacimi
# Thibaud Le Du - Gaspard Lauras

# Code entraînement IA
# Implique les programmes "env", "model" et "render"
# Réseau de neurones à deux couches cachées (10 neurones puis 3 neurones)
# Reinforcement learning

# Décommenter les dernières lignes de code pour :
# Afficher le diagramme des "rewards" en fonction des générations
# Afficher ensuite la partie jouée avec la meilleure configurations des poids obtenue

# Génère les fichiers ".npy" des meilleurs poids à l'issue de l'entraînement

import numpy as np
import matplotlib as plt
from env import CarEnv



class Execute:
    def __init__(self,nomFond,epochs=80):


        ########################################## 
        #Class DescreteAgent (init | policy | update | train | freeze | test)
            #init : paramétrage
            #policy : combinaison linéaire return choix action
            #update : set params
            #train : work policy avec states et params
            #freeze : update des best params
            #test : work policy avec states et best params
        #nomFond = "Sircuibo.png" 


        nbEpochs = epochs                                                       # Nombre de parties à simuler au total [à modifier]
        
        class DiscreteAgent:                                                           
                
            def __init__(self, input_dim, output_dim, hidden_dim):
                                                                        
                self.hidden = hidden_dim                                                
                self.input = input_dim
                self.output = output_dim
                self.params = np.random.rand(self.hidden,self.input+1+ self.output)     
                self.dim = 11 * 17
                 
            def policy(self, state, params):
                # States
                sensor_mid = state[0]
                sensor_r = state[1]
                sensor_l = state[2]
                sensor_ff = state[3]
                sensor_ll = state[4]
                
                w = np.reshape(params,(11, 17))                                 # On veut "10+1" lignes et 17 colonnes
                
                tab_z = []                                                             
                tab_y = []                              
                
                for x in range (0, self.hidden) :                               # Première couche : 10 neurones
                    op = w[x,0]+ w[x,1]*sensor_mid+ w[x,2]*sensor_r+w[x,3]*sensor_l + w[x,4]*sensor_ff+ w[x,5]*sensor_ll                           
                    z = np.tanh(op) 
                    tab_z.append(z)
                                                                                        
                for k in range (0, self.output) :                               # Deuxième couche : 3 neurones    
                    y = w[k,6] + w[k,7]*tab_z[0]+ w[k,8]*tab_z[1] + w[k,9]*tab_z[2] + w[k,10]*tab_z[3]+ w[k,11]*tab_z[4] + w[k,12]*tab_z[5] + w[k,13]*tab_z[6]+ w[k,14]*tab_z[7]+ w[k,15]*tab_z[8] + w[k,16]*tab_z[9]  
                    tab_y.append(y)        

                action = np.argmax(tab_y)

                return action                                                   # 3 possibilités : Gauche - Droite - Ne rien faire
            
            def update(self, params):
                self.params = params
                
            def train(self, state):
                return self.policy(state, self.params)
            
            def freeze(self, best):
                self.best = best.copy()
                
                
            def test(self, state):
                return self.policy(state, self.best)
        ##
        #Cross-entropy method : 
            #def policy_search(env, agent, epochs=100, batch=100, elite=0.2, horizon=1000, repeat=2, parallel=True, render=False)
            #policy_search : gère les params et returns history
            #[appel à : rollout, elite_parameters, freeze]
            
        def policy_search(env, agent, epochs= 80, batch=1, elite=0.2, horizon=2000, repeat=1, parallel=True, render=True):
            # Settings
            n_elites    = int(batch * elite)
            extra_std   = 2.0
            extra_decay = epochs * 0.8
            
            # Initalization
            mean = np.zeros(agent.dim)
            std  = np.ones(agent.dim)
            
            # Best score overall
            best_score = -np.inf
            
            # Training
            history = {"reward": [], "mean": [], "std": []}
            for it in range(epochs):
                
                # Compute the noisy covariance
                extra_cov = max(1.0 - it / extra_decay, 0) * extra_std**2
                cov = np.diag(std**2 + extra_cov)

                # Randomly draw several sets of parameters                      ''' Create random params'''
                params = np.random.multivariate_normal(mean, cov, batch)

                # Estimate the score for each set of parameters
                scores = rollout(env, agent, params, repeat, horizon, parallel, render)
                    
                # Learn from the top-performing sets of parameters
                mean, std, best = elite_parameters(params, scores, n_elites)
                
                # Save the best parameters in a npy file
                if scores.max() >= best_score:
                    best_score = scores.max()
                    agent.freeze(best) 
                    if nomFond == "Sircuibo.png":                               # Sauvegarde des meilleurs poids dans un fichier
                        np.save('BestParamsSircuibo.npy',best)  
                    elif nomFond == "CIRCUIT11.png": 
                        np.save('BestParamsCIRCUIT11.npy',best)                               
                    
                # Track the history
                history["reward"].append(scores.mean())
                history["mean"].append(mean.copy())
                history["std"].append(std.copy())

                # Print the info
                if (it+1) % 10 == 0:
                    print("Epoch {:3d}/{:3d} - Score (mean/best): {:2.3f} / {:2.3f}".format(it+1, epochs, scores.mean(), best_score))
            
            return history
        ##
        # Rollout : 
                #def rollout(env, agent, params, repeat, horizon, parallel, render)
                #rollout : gère les scores associés et returns scores
                #[appel à : evaluate_score]

        def rollout(env, agent, params, repeat, horizon, parallel, render):
           
            # Number of rollouts
            batch = params.shape[0]

            # Initialize the vector of scores
            scores = np.zeros(batch)
            
            # Play several episodes with the same sets of parameters
            for _ in range(repeat):
                if parallel:
                    scores += evaluate_score(env, agent, params, horizon, render)
                else:
                    for i in range(batch):
                        scores[i] += evaluate_score(env, agent, params[i], horizon, render)
            
            # Average the scores
            scores /= repeat

            return scores
        ##
        #Play game and return score : 
            #def evaluate_score(env, agent, params, horizon, render)
            #evaluate_score : joue partie, returns rewards
            #[appel à : play_episode]

        def evaluate_score(env, agent, params, horizon, render):
            
            # Set the agent's parameters
            agent.update(params)
            
            # Play an episode
            episode = play_episode(env, agent.train, horizon, render)
            
            # Get the rewards
            rewards = episode["rewards"]
                    
            # Compute the score for each episode. It's the sum of rewards collected during each episode.
            total = np.sum(rewards,axis=0) 
            
            return total
        ##
        #State-action-reward loop : 
            #def play_episode(env, policy, horizon=1000, render=False)
            #play_episode : gère state-action-reward loop
            #[appel à : policy, | env.reset, env.step, env.render]

        def play_episode(env, policy, horizon=1000, render=False):
            
            episode = {"states": [], "actions": [], "rewards": [], "frames": []}
                
            state = env.reset()                                                         
            
            for _ in range(horizon):
                
                action = policy(state)                                                  
                
                episode["states"].append(state)
                episode["actions"].append(action)
                
                state, reward, done, _ = env.step(action)
                
                episode["rewards"].append(reward)
                
                if render: 
                    frame = env.render()
                    episode["frames"].append(frame if isinstance(frame, np.ndarray) else env.render('rgb_array'))
                    
                if done: break
                    
            env.close()
            
            make_array = np.ma.MaskedArray if isinstance(state, np.ma.MaskedArray) else np.array
            episode["states"]  = make_array(episode["states"])
            episode["actions"] = make_array(episode["actions"])
            episode["rewards"] = make_array(episode["rewards"])
            
            return episode
        ##
        #Sorts the sets of parameters according to their score
        #Computes the mean and standard deviation of the top-20% sets of parameters
        #Selects the best set of parameters     
            #def elite_parameters(params, scores, n_elites)                                                                                                                                     
            #returns  mean, std, and best params

        def elite_parameters(params, scores, n_elites):
            
            # Compute the indices that would sort the vector 'scores'
            idx = np.argsort(scores)
            
            # Take the indices associated to the 'n_elites' highest scores
            idx = idx [-n_elites:]
                
            # Select the rows of 'params' associated to highest scores
            elites = params[idx, : ]
            
            # Compute the mean and std of 'elites' along the columns 
            mean = np.mean(elites, axis=0)
            std  = np.std(elites, axis=0)
            
            # Select the row of 'params' with the best score
            best = params[np.argmax(scores), : ] #params[np.amax(idx), : ]
            
            return mean, std, best
        ##
        # Programme d'entraînement de l'IA :

        # Entraînement
        agent = DiscreteAgent(input_dim=5, output_dim=3, hidden_dim=10)
        env = CarEnv(nomFond)
        env.seed(0)
        np.random.seed(0)
        history = policy_search(env, agent, epochs = nbEpochs)
         
        # Affichage graphe "rewards" : 
        #import matplotlib.pyplot as plt
        #plt.plot(history["reward"])
        #plt.show()

        # Affichage meilleure partie : 
        #episode = play_episode(env, agent.test, render=True)
        #plt.imshow(episode["frames"][-1])
        #plt.title("Score: " + str(episode["rewards"].sum()))
        #plt.show()




