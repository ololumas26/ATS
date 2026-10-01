# services/calc_cossin_service.py
# Cálculo da similaridade do cosseno entre dois vetores.


class CosineSimilarity:

    def __init__(self, vetor_1 : list, vetor_2):

        if not vetor_1 or not vetor_2:
            raise Exception("Ambos os vetores são obrigatórios")
        
        if len(vetor_1) != len(vetor_2):
            raise Exception("O cálculo da similaridade do cosseno exige 2 vetores de igual tamanho")

        self.vetor_1 = vetor_1
        self.vetor_2 = vetor_2

  
    def _calc_scalar_product(self):

        scalar_product = 0

        for i in range(0, len(self.vetor_1)):
            scalar_product += self.vetor_1[i] * self.vetor_2[i]

        return scalar_product

   
    def _calc_magnitude(self, embedding : list):

        magnitude = 0

        for value in embedding:
            magnitude += value ** 2

        return magnitude ** (1/2)


    def calc_cossin_similarity(self):

        scalar = self._calc_scalar_product()
        magnitude = self._calc_magnitude(self.vetor_1) * self._calc_magnitude(self.vetor_2)

        return scalar / magnitude
