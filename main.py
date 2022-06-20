import datetime

def convertDNI(data): #переводит разницу во времени в кол-во дней типа int
    data = str(data)
    data = data.split()
    data = data[0]
    return int(data)

def converDate(date): #перевод введенной даты в тип datetime.date
    razdelitel = date[2]
    date = date.split(razdelitel)
    years = int(date[2])
    months = int(date[1])
    days = int(date[0])
    date = datetime.date(years, months, days)
    return date

def dekret(pStart, count): #первый декрет
    
    dekretStart = input('Введите дату начала декрета в формате чч мм гггг:\n') #пользователб вводит дату 1го декрета
    dekretStart = converDate(dekretStart)                 #перевод введенной даты в тип datetime.date
    
    
    d = dekretStart - pStart #количество дней от начала периода до декрета
    d = convertDNI(d)
    count -= d #счетчик дней, по достижении 365, период закроется
    if d > 365:#проверка на количество дней в периоде
        print (f'ОШИБКА! Проверьте правильность ввода дат, скорее всего период закрыт, т.к. отработано {d} д.')
        main()
    print(f'Отработано {d} д., осталовь отработать {count} д.')
    
    dekretEnd = input('Введите дату окончания декрета в формате чч мм гггг:\n') #пользователб вводит дату 1го декрета
    dekretEnd = converDate(dekretEnd)                     #перевод введенной даты в тип datetime.date

    endPeriod = dekretEnd + datetime.timedelta(days=(count)) #вычисляем дату закрытия рабочего периода
    print('*****************************************************')
    print(f"""Начало периода: {pStart}
Уход в декрет: {dekretStart}
Отработано дней до ухода в декрет: {d} д.
Осталось отработать до закрытия периода {count} д.
Выход из декрета {dekretEnd}
Период закроется соотвественно через {count} д., это будет {endPeriod}
Итог - начало периода {pStart}, конец {endPeriod}\n\
*****************************************************""")
    return count, dekretEnd, dekretStart  #возвращаем счетчик и дату закрытия декрета на тот случай, если до закрытия периода был еще 1 декрет

def dekretRep (pStart, count, dEnd, dst): 
    print(f"""*****************************************
    Краткая информация по предыдущему декрету:
Начало периода: {pStart}
Начало первого декрета: {dst}
Окончание первого декрета: {dEnd}
Осталось отработать до закрытия периода: {count} д.
*****************************************""") #краткая воодная информация

    dekretStart = input('Введите дату начала нового декретав формате чч мм гггг:\n') #пользователб вводит дату очередного декрета
    dekretStart = converDate(dekretStart)                      #перевод введенной даты в тип datetime.date

    d = dekretStart - dEnd #количество дней от закрытия старого декрета до открытия нового декрета
    d = convertDNI(d)      #переводит разницу во времени в кол-во дней типа int
    countOld = count
    dOld = 365 - countOld
    count -= d             #обновляем счетчик (вычитаем время с даты закрытия старого декрета до открытия нового декрета)
    print (f'Отработано с момента выхода из предыдущего декрета до ухода в новый декрет {d} д.,\n\
осталовь отработать до закрытия периода {count} д.')

    dekretEnd = input('Введите дату окончания декрета в формате чч мм гггг:\n') #пользователб вводит дату закрытия очередного декрета
    dekretEnd = converDate(dekretEnd)                     #перевод введенной даты в тип datetime.date

    endPeriod = dekretEnd + datetime.timedelta(days=(count))  #вычисляем дату закрытия рабочего периода
    print('_____________________________________________________')
    print('*****************************************************')
    print('_____________________________________________________')
    print(f"""Начало периода: {pStart}
Дата ухода в первый декрет: {dst}
Отработано перед первым декретом {dOld} д.
Дата выхода из первого декрета: {dEnd}
______________________________________
Дата ухода во 2й декрет: {dekretStart}
Отработано дней до ухода во 2й декрет: {d} д.
Осталось отработать до закрытия периода, после выхода из декрета {count} д.
Дата выхода из 2го декрета {dekretEnd}
Период закроется соотвественно через {count} д., это будет {endPeriod}
Итог - начало периода {pStart}, конец {endPeriod}
*****************************************""")
    return count, dekretEnd #возвращаем счетчик и дату закрытия декрета на тот случай, если до закрытия периода был еще 1 декрет

def raschet (dekretEnd, count):
    otpdni = int(input('Укажите количество дней отпуска положенных сотруднику в данном периоде\n'))
    ostatki = int(input('Укажите количество неотгулянных дней из предыдущих периодов (если есть)\n'))
    vibrdni = int(input('Укажите сколько дней сотрудник отгулял в текущем периоде\n'))
    endPeriod = input('Введите дату увольнения в формате чч мм гггг\n') #пользователб вводит дату очередного декрета
    endPeriod = converDate(endPeriod)              #перевод введенной даты в тип datetime.date
    if endPeriod < dekretEnd:
        dekretEnd = endPeriod
        d3 = 0
    else:
        d3 = endPeriod - dekretEnd
        d3 = convertDNI(d3)
    count -= d3
    count = 365 - count
    compensacia = (otpdni / 12 / 30) * count + ostatki - vibrdni
    print(f"Отработано {count}д.")
    print("Компенсация составит: " + '%.2f' % (compensacia) + 'д.')
    print('*****************************************************')

def main():
    while True:
        try:
            count = 365
            periodStart = input('Добро пожаловать!\nВведите дату начала периода в формате чч мм гггг\n')
            periodStart = converDate(periodStart)
            zapros = input('Если в текущем периоде был декрет - жми "1"\n\
Если сотрудник уволился до закрытия периода - жми "2"\n')
            if zapros == '1':
                count, dekretEnd, dst = dekret(periodStart, count)
            elif zapros == "2":
                raschet (periodStart, count)
                main()

            zapros = input('Если в текущем периоде был еще 1 декрет, нажмите "1"\n\
Для перехода к расчету компенсации нажмите "2"\n\
Для перезапуска программы нажмите "0"\n')
            if zapros == '1':
                    count, dekretEnd = dekretRep(periodStart,count, dekretEnd, dst)
            elif zapros == "0":
                print ('Перезапуск')
                print('*****************************************************')
                main()
            elif zapros == "2":
                raschet (dekretEnd, count)
                main()

            zapros = input('Для перехода к расчету компенсации нажмите "2"\n\
Для перезапуска программы нажмите "0"\n')
            if zapros == "2":
                raschet(dekretEnd, count)
                main()
            elif zapros == "0":
                print ('Перезапуск')
                print('*****************************************************')
                main()
        except Exception:   
            print('Проверьте правильность ввода данных')
            main()

main()