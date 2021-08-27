import numpy as np

INF_POINT = None


class EllipticCurve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p
        self.points = []
        self.definePoints()
        self.G = (8, 113)  # G is our generator point lying on our curve E(2,3,211)

    def definePoints(self):
        self.points.append(INF_POINT)
        for x in range(self.p):
            for y in range(self.p):
                if self.equalModp(y * y, x * x * x + self.a * x + self.b):
                    self.points.append((x, y))

    def addition(self, P1, P2):
        if P1 == INF_POINT:
            return P2
        if P2 == INF_POINT:
            return P1

        x1 = P1[0]
        y1 = P1[1]
        x2 = P2[0]
        y2 = P2[1]

        if self.equalModp(x1, x2) and self.equalModp(y1, -y2):
            return INF_POINT

        if self.equalModp(x1, x2) and self.equalModp(y1, y2):
            u = self.reduceModp((3 * x1 * x1 + self.a) * self.inverseModp(2 * y1))
        else:
            u = self.reduceModp((y1 - y2) * self.inverseModp(x1 - x2))

        v = self.reduceModp(y1 - u * x1)
        x3 = self.reduceModp(u * u - x1 - x2)
        y3 = self.reduceModp(-u * x3 - v)

        return (x3, y3)

    def pointMultiplication(self, P, k):
        x = P[0]
        y = P[1]
        for i in range(k - 1):
            (x, y) = self.addition((x, y), P)
        return (x, y)

    def numberPoints(self):
        return len(self.points)

    def discriminant(self):
        D = -16 * (4 * self.a * self.a * self.a + 27 * self.b * self.b)
        return self.reduceModp(D)

    def printPoints(self):
        print(self.points)

    # helper functions

    def reduceModp(self, x):
        return x % self.p

    def equalModp(self, x, y):
        return self.reduceModp(x - y) == 0

    def inverseModp(self, x):
        for y in range(self.p):
            if self.equalModp(x * y, 1):
                return y
        return None

    def user1_key(self, Pu2):
        r1 = 7  # This is the private key of user 1
        self.Pu1 = self.pointMultiplication(self.G, r1)  # Public Key of User1

    def user2_keys(self):
        r2 = 13  # This is the private key of user 2
        Pu2 = self.pointMultiplication(self.G, r2)  # Public Key of User2
        return (Pu2)

    def encryption_user1(self, random, public_key, message="hello"):
        """ This Function Encrypts a Given Message into a List of points lying on the curve For A given Public Key. """
        # First We Convert message to octal and map each octal digit to unique point on curve

        decode_random = random
        cipher_point = self.pointMultiplication(public_key, decode_random)
        cipher1 = self.pointMultiplication(self.G, random)
        self.points_mapped_to_octal = {}
        octal_digits = [0, 1, 2, 3, 4, 5, 6, 7]
        encoded_point = []
        for octal in octal_digits:
            j = 0
            flag = 1
            flag2 = 1
            while j < 9 and flag != 0:
                j = j + 1
                x_coord = decode_random * octal + j
                actual_x_coord = 1
                while actual_x_coord < len(self.points) and flag2 != 0:
                    if x_coord == self.points[actual_x_coord][0]:
                        encoded_point.append((self.points[actual_x_coord], octal)) # Mapping octal digits to actual pts
                        flag = 0
                        flag2 = 0
                    else:
                        actual_x_coord = actual_x_coord + 1
        for f in range(len(encoded_point)):
            self.points_mapped_to_octal[encoded_point[f][1]] = encoded_point[f][0]
        self.message_points = []
        a = np.base_repr(int(message, 36), base=8)  # Here We Convert our message to octal format
        n = int(a)
        while n != 0:
            i = n % 10
            self.message_points.append(self.points_mapped_to_octal[i])
            n = n // 10

        encrypted_message = []
        for i in range(len(self.message_points)):
            encrypted_message.append(self.addition(self.message_points[i], cipher_point))
        print('Encrypted_message')
        print(cipher1)
        encrypted_message.append(cipher1)
        return (encrypted_message)

    def decrpyt_user2(self, privateKey, encrypted_points, random=7):
        """ This function Decrypts a list of points into a Words using the users private key"""
        converted_to_base8 = []
        base8number = 0
        l = len(encrypted_points)
        subtraction_point = self.pointMultiplication(encrypted_points[l - 1], privateKey)
        subtraction_point = (subtraction_point[0], -subtraction_point[1])
        for i in range(l - 2, -1, -1):
            encrypted_points[i] = self.addition(encrypted_points[i], subtraction_point)
            converted_to_base8.append(int((encrypted_points[i][0] - 1) / random))
            base8number = base8number * 10 + int((encrypted_points[i][0] - 1) / random)
        base8_str = f'{base8number}'
        base10 = int(base8_str, base=8)
        word = np.base_repr(base10, base=36)
        print(word)
        return(word)
