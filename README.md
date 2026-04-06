# IA

Taller de tetravex

  El orden membero → adyacencia → neq por celda es correcto. MiniKanren procesa los goals en orden, entonces:                                                                                               
  1. membero asigna un valor candidato                                                                                                                                                                     
  2. la adyacencia lo poda inmediatamente si no encaja con el vecino                                                                                                                                     
  3. neq evita repetición