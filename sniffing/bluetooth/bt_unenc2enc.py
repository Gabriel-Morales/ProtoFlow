#!/usr/bin/env python3

'''
Use scapy to modify unencrypted bluetooth hci.log 
    that has been converted to hci.pcap using
    wireshark into encrypted hci log using AES_CCM.
    Encrypts payload of all packets with a payload

Helps verify packet size consistency via output
NOTE - Will crash by design if modified packets
    are not the same size as originals.
    Sizes should, however, always be equal.
'''

import scapy
from scapy.all import *
from Crypto.Cipher import AES
#from Crypto.Util.Padding import pad

def expand(x):
    yield x
    while x.payload:
        x = x.payload
        yield x

def get_packet_layers(packet):
    counter = 0
    while True:
        layer = packet.getlayer(counter)
        if layer is None:
            break

        yield layer
        counter += 1

def print_packet_layers(packet):
    layers = get_packet_layers(packet)
    for layer in layers:
        print(layer.name, end=' # ')
    print()



def main():

    # Load input pcap file
    cap_filename = "btsnoop_hci_unencrypted.pcap"
    bt_packets = rdpcap(cap_filename)

    # Output file name and list for storing modified packets
    out_filename = "btsnoop_hci_encrypted.pcap"
    out_packets = []


    counter = 0
    for packet in bt_packets:
        key = b'abcdefghijklmnop'
        #enc_cipher = AES.new(key, AES.MODE_CCM)

        if packet.haslayer("Raw"):
            # Ciphers must be generated per packet
            enc_cipher = AES.new(key, AES.MODE_CCM)
            unenc_payload_length = len(packet["Raw"])

            # Unencrypted payload
            unencrypted_payload_1 = packet["Raw"]
            unencrypted_packet_length = len(packet)

            # Encrypt payload using AES CCM
            packet["Raw"] = scapy.packet.Raw(enc_cipher.encrypt(bytes(packet["Raw"])))
            encrypted_payload_1 = packet["Raw"]
            enc_payload_length = len(packet["Raw"])
            encrypted_packet_length = len(packet)

            # This is an example of storing the unencrypted data from encrypted data
            #   Only uncomment if intending to use this value
            #   NOTE - Consecutive enc_ciphers or d_ciphers must not be uncommented
            #   at the same time
            #d_cipher = AES.new(key, AES.MODE_CCM, enc_cipher.nonce)
            #print(scapy.packet.Raw(d_cipher.decrypt(bytes(packet["Raw"]))))

            #################################################################
            ## Uncomment these lines to explore unencrypted data comparison

            ## Decrypted payload
            #d_cipher = AES.new(key, AES.MODE_CCM, enc_cipher.nonce)
            #unencrypted_payload_2 = d_cipher.decrypt(bytes(packet["Raw"]))
            ##print(d_cipher.decrypt(bytes(packet["Raw"])))

            ## Re-encrypted payload
            #enc_cipher = AES.new(key, AES.MODE_CCM)
            #encrypted_payload_2 = enc_cipher.encrypt(bytes(packet["Raw"]))
            ##print(enc_cipher.encrypt(bytes(packet["Raw"])))

            ## The unencrypted payloads should be the same
            #print(unencrypted_payload_1)
            #print(unencrypted_payload_2)
            #print(encrypted_payload_1)
            #print(encrypted_payload_2)
            #################################################################

            print("\t\tEnc\tUnenc")
            print("Payload lengths: {}\t{}".format(enc_payload_length, unenc_payload_length))
            # Exit to help identify problems. Should never happen
            if(unenc_payload_length != enc_payload_length) \
              or (unencrypted_packet_length != encrypted_packet_length):
                print("Mismatched payload or packet lengths")
                print("Encrypted packet:\t{}".format(encrypted_packet_length))
                print("Unencrypted packet:\t{}".format(unencrypted_packet_length))

                print("Encrypted payload:\t{}".format(encrypted_payload_1))
                print("Unencrypted payload:\t{}".format(unencrypted_payload_1))
                sys.exit(1)


            # Store the encryption modification in the pcap
        out_packets.append(packet)

        counter += 1

    # Write modified pcap to disk
    wrpcap(out_filename, out_packets)
if __name__ == '__main__':
    main()
