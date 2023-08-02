import binascii 
import struct 

offset = 446


def big_endian_to_little_endian(big_endian_data):
     # 빅엔디안 바이너리 데이터의 바이트 순서를 반대로 변경하여 리틀엔디안으로 변환
    num_bytes = len(big_endian_data)
    little_endian_data = b''.join([big_endian_data[num_bytes - i - 1:num_bytes - i] for i in range(num_bytes)])

    return little_endian_data


def bytes_to_int(byte_data):
    # 바이트 문자열을 정수로 변환
    integer_value = int.from_bytes(byte_data, byteorder='big', signed=False)
    return integer_value

def int_to_bytes(integer_value):
    # 정수를 바이트 문자열로 변환
    byte_data = integer_value.to_bytes((integer_value.bit_length() + 7) // 8, byteorder='big', signed=False)
    return byte_data
        


def read_file(file_path):
    type = False 
    
    with open(file_path, 'rb') as file:
  
        # 지정한 offset만큼 파일 포인터를 이동시킨다.  
        file.seek(offset)
        
        # 데이터를 읽기 
        data = file.read()
        
        # binary data를 hex 값인 문자열을 변환합니다. 
        #hex_data = binascii.hexlify(data).decode('utf-8')
        
  
        fpartition = data[0:16]
        print("====================================")
        
        jump = 0
        while(True):

            fpartition = data[jump:jump+16]
            if fpartition[4] == 7:
                print("partition table entry")
                LBA_ADDRESS = fpartition[8:12]
                # 빅엔디안을 리틀엔디안으로 변환 
                LBA_ADDRESS = big_endian_to_little_endian(LBA_ADDRESS)
                
                # 바이트 문자열을 정수로 변환 
                INT_LBA_ADDRESS = bytes_to_int(LBA_ADDRESS)
                INT_LBA_ADDRESS = INT_LBA_ADDRESS * 512 

                
                LBA_ADDRESS = int_to_bytes(INT_LBA_ADDRESS)
                LBA_ADDRESS_hex= binascii.hexlify(LBA_ADDRESS).decode('utf-8')
                print("File System LBA_ADDRESS", LBA_ADDRESS_hex)
                
                # Numbers of sector 사이즈 구하기 
                f_size = fpartition[12:16]
                f_size = bytes_to_int(f_size)
                f_size = f_size * 512 

                
                f_size = int_to_bytes(f_size)
                f_size= binascii.hexlify(f_size).decode('utf-8')
                print("File System Size", f_size)
                
                # 해당 LBA_ADDRESS로 주소 이동
                LBA_ADDRESS = LBA_ADDRESS
                LBA_ADDRESS= binascii.hexlify(LBA_ADDRESS).decode('utf-8')
                
                file.seek(int(LBA_ADDRESS, 16) + 3)
                data_type = file.read()
                
                print("File System Type",data_type[0:4])
                jump += 16
                fpartition = data[jump:jump+16]
    
                print("====================================\n")
                
            if fpartition[4] == 5:
                print("- EBR File System -")
                
                LBA_ADDRESS = fpartition[8:12]
                # 빅엔디안을 리틀엔디안으로 변환 
                LBA_ADDRESS = big_endian_to_little_endian(LBA_ADDRESS)
                
                # 바이트 문자열을 정수로 변환 
                INT_LBA_ADDRESS = bytes_to_int(LBA_ADDRESS)
                INT_LBA_ADDRESS = INT_LBA_ADDRESS * 512 

                
                LBA_ADDRESS = int_to_bytes(INT_LBA_ADDRESS)
                LBA_ADDRESS_hex= binascii.hexlify(LBA_ADDRESS).decode('utf-8')
                LBA_ADDRESS_origin = int.from_bytes(LBA_ADDRESS, byteorder='big', signed=False)
                
            
                file.seek(int(LBA_ADDRESS_hex, 16) + 446)
                print("File System LBA_ADDRESS", LBA_ADDRESS_hex)
                nbr_type = file.read()
                
                while(True):
                    file.seek(int(LBA_ADDRESS_hex, 16) + 446)
                    nbr_type = file.read()
                    if(nbr_type[4] == 7) : 
                        
                        
                        real_ADDRESS = nbr_type[8:12]
                        LBA_ADDRESS  = int(LBA_ADDRESS_hex, 16)
                   
                        
                        # 빅엔디안을 리틀엔디안으로 변환 
                        real_ADDRESS=  big_endian_to_little_endian(real_ADDRESS)
                        real_ADDRESS = int.from_bytes(real_ADDRESS, byteorder='big', signed=False) * 512
                        
                        
                        real_ADDRESS += LBA_ADDRESS
                        
                        real_ADDRESS = int_to_bytes(real_ADDRESS)
                        real_ADDRESS_hex= binascii.hexlify(real_ADDRESS).decode('utf-8')

                        print("File System REAL_MBR_ADDRESS", real_ADDRESS_hex)
                        
                        
                    if(nbr_type[20] == 5) : 
                        
                        next_ADDRESS = nbr_type[24:28]
                        
                    
                        # 빅엔디안을 리틀엔디안으로 변환 
                        next_ADDRESS=  big_endian_to_little_endian(next_ADDRESS)
                    
                        next_ADDRESS = int.from_bytes(next_ADDRESS, byteorder='big', signed=False)

                        next_ADDRESS = next_ADDRESS * 512
                        next_ADDRESS += LBA_ADDRESS_origin
                        
                        next_ADDRESS = int_to_bytes(next_ADDRESS)
                    
                
                        next_ADDRESS_hex= binascii.hexlify(next_ADDRESS).decode('utf-8')
                        print("File System next_MBR_ADDRESS ", next_ADDRESS_hex)
                        
                        
                        
                        print("===============")
                    if(nbr_type[20] == 0) : 
                        print("====== 끝입니다 ====")
                        type = True
                        break
                
                  
                    LBA_ADDRESS_hex = next_ADDRESS_hex
               
                    
            if type == True :
                break
            
            jump += 16
            
            
        
      
        
    
if __name__ == "__main__":
    
    file_path = '../mbr_128.dd'
    print("실행 파일", file_path.split('/')[-1])
    file_content = read_file(file_path)
