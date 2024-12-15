import cv2

def isGrayScale():
    if d == 1:
        return True
    for i in range(0, h):
        for j in range(0, w):
            pixel = image[i, j]
            if pixel[0] != pixel[1] != pixel[2]:
                return False
            else:
                continue
    return True

def encrypt():
    cv2.imshow('cover', image)
    bin_len = len(bin_string)
    key_len = len(key)
    binCurr = 0
    keyCurr = -1
    if not isBnw:
        for i in range(0, h):
            for j in range(0, w):
                keyCurr = (keyCurr + 1) % key_len
                if ((image[i, j, 0] & 1) ^ key[keyCurr]) == 0:
                    image[i, j, 1] = (image[i, j, 1] & ~1) | int(bin_string[binCurr])
                    binCurr += 1
                else:
                    image[i, j, 2] = (image[i, j, 2] & ~1) | int(bin_string[binCurr])
                    binCurr += 1
                if binCurr == bin_len:
                    break
            if binCurr == bin_len:
                break

    else:
        for i in range(0, h):
            for j in range(0, w):
                keyCurr = (keyCurr + 1) % key_len
                a = int(bin_string[binCurr]) ^ key[keyCurr]
                image[i, j] = (image[i, j] & ~1) | a
                binCurr += 1
                if binCurr == bin_len:
                    break
            if binCurr == bin_len:
                break

    if binCurr != bin_len:
        print('--> Image Capacity exceeded!')
    else:
        cv2.imwrite('embed.png', image)
    cv2.imshow('stego', image)


def decrypt():
    cv2.imshow('stego', image)
    embed_string = ''
    key_len = len(key)
    binCurr = 0
    keyCurr = -1
    if not isBnw:
        for i in range(0, h):
            for j in range(0, w):
                keyCurr = (keyCurr + 1) % key_len
                if (image[i, j, 0] & 1) ^ key[keyCurr] == 0:
                    embed_string += str(image[i, j, 1] & 1)
                    binCurr += 1
                else:
                    embed_string += str(image[i, j, 2] & 1)
                    binCurr += 1
                if binCurr == stream_len:
                    break
            if binCurr == stream_len:
                break
    else:
        for i in range(0, h):
            for j in range(0, w):
                keyCurr = (keyCurr + 1) % key_len
                a = (image[i, j] & 1) ^ key[keyCurr]
                embed_string += str(a)
                binCurr += 1
                if binCurr == stream_len:
                    break
            if binCurr == stream_len:
                break

    if binCurr != stream_len:
        print('--> Message length entered is beyond image capacity!')
    return embed_string



if __name__ == "__main__":
    secretData = open('SecretKey.txt', 'r')
    data = secretData.read()
    key = [int(i) for i in data.split(' ')]

    while 1:
        choice = int(input("Encrypt-1 or Decrypt-2 : "))
        if choice == 1:
            cover_path = input("Enter cover image path: ")
            image = cv2.imread(cover_path)
            (h, w, d) = image.shape
            isBnw = isGrayScale()
            if isBnw:
                print('--> GrayScale Image!')
            else:
                print('--> RGB color Image!')
            if d == 3 and isBnw:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            msg = str(input("Enter secret message (Enter 0 for default message): "))
            if msg == '0':
                msg = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore etdolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
                print('--> Default Message: '+ msg)
            byte_array = msg.encode()
            binary_int = int.from_bytes(byte_array, "big")
            bin_string = bin(binary_int)
            bin_string = bin_string[0] + bin_string[2:]
            print('=> Encoded Binary String: ' + bin_string)
            print('--> Stego Image written into embed.png file for further decryption!')
            encrypt()
        else:
            stego_path = input("Enter stego image path: ")
            image = cv2.imread(stego_path)
            (h, w, d) = image.shape
            isBnw = isGrayScale()
            if isBnw:
                print('--> GrayScale Image!')
            else:
                print('--> RGB color Image!')
            if d == 3 and isBnw:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            msg_len = int(input("Enter secret message length (Enter 0 for default length): "))
            if msg_len == 0:
                msg_len = 444
            stream_len = msg_len * 8
            embed = decrypt()
            print("=> Recovered Binary String: " + embed)
            binary_int = int(embed, 2)
            byte_number = binary_int.bit_length() + 7 // 8
            binary_array = binary_int.to_bytes(byte_number, "big")
            ascii_text = binary_array.decode()
            print('=> secrete Message:' + ascii_text)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
