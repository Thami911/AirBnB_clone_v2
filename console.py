#!/usr/bin/python3
"""Describes the HBNB console."""
import cmd
from shlex import split
from models import storage
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review




class HBNBCommand(cmd.Cmd):
    """Describes the HolbertonBnB command interpreter."""


    prompt = "(hbnb) "
    __classes = {"BaseModel", "State", "User", "city",
                 "Place", "Amenity", "Review"}

    def emptyline(self):
        """Ignore empty spaces."""
        pass


    def do_quit(self, line):
        """Quit command to exit the program."""
        return True


    def do_EOF(self, line):
        """EOF signal to exit the program."""
        print("")
        return True


    def do_create(self, line):
        """Usage: create <class> <key 1>=<value 2> <key 2>=<value 2> ...
        Create a new class instance with given keys/values and print its id.
        """
        try:
            if not line:
                raise SyntaxError()
            mc_list = line.split(" ")


            kwargs = {}
            for i in range(1, len(mc_list)):
                key, value = tuple(mc_list[i].split("="))
                if value[0] == '"':
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except (SyntaxError, NameError):
                        continue
                kwargs[key] = value


            if kwargs == {}:
                obj = eval(mc_list[0])()
            else:
                obj = eval(mc_list[0])(**kwargs)
                storage.new(obj)
            print(obj.id)
            obj.save()


        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")


    def do_show(self, line):
        """Prints the string representation of an instance
        Exceptions:
            SyntaxError: when there is no args given
            NameError: when there is no object taht has the name
            IndexError: when there is no id given
            KeyError: when there is no valid id given
        """
        try:
            if not line:
                raise SyntaxError()
            mc_list = line.split(" ")
            if mc_list[0] not in self.__classes:
                raise NameError()
            if len(mc_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = mc_list[0] + '.' + mc_list[1]
            if key in objects:
                print(objects[key])
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")


    def do_destroy(self, line):
        """Deletes an instance based on the class name and id
        Exceptions:
            SyntaxError: when there is no args given
            NameError: when there is no object taht has the name
            IndexError: when there is no id given
            KeyError: when there is no valid id given
        """
        try:
            if not line:
                raise SyntaxError()
            mc_list = line.split(" ")
            if mc_list[0] not in self.__classes:
                raise NameError()
            if len(mc_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = mc_list[0] + '.' + mc_list[1]
            if key in objects:
                del objects[key]
                storage.save()
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")


    def do_all(self, line):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        if not line:
            o = storage.all()
            print([o[k].__str__() for k in o])
            return
        try:
            args = line.split(" ")
            if args[0] not in self.__classes:
                raise NameError()


            o = storage.all(eval(args[0]))
            print([o[k].__str__() for k in o])


        except NameError:
            print("** class doesn't exist **")


    def do_update(self, line):
        """Updates an instanceby adding or updating attribute
        Exceptions:
            SyntaxError: when there is no args given
            NameError: when there is no object taht has the name
            IndexError: when there is no id given
            KeyError: when there is no valid id given
            AttributeError: when there is no attribute given
            ValueError: when there is no value given
        """
        try:
            if not line:
                raise SyntaxError()
            mc_list = split(line, " ")
            if mc_list[0] not in self.__classes:
                raise NameError()
            if len(mc_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = mc_list[0] + '.' + mc_list[1]
            if key not in objects:
                raise KeyError()
            if len(mc_list) < 3:
                raise AttributeError()
            if len(mc_list) < 4:
                raise ValueError()
            v = objects[key]
            try:
                v.__dict__[mc_list[2]] = eval(mc_list[3])
            except Exception:
                v.__dict__[mc_list[2]] = mc_list[3]
                v.save()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")
        except AttributeError:
            print("** attribute name missing **")
        except ValueError:
            print("** value missing **")


    def count(self, line):
        """count the number of instances of a class
        """
        counter = 0
        try:
            mc_list = split(line, " ")
            if mc_list[0] not in self.__classes:
                raise NameError()
            objects = storage.all()
            for key in objects:
                name = key.split('.')
                if name[0] == mc_list[0]:
                    counter += 1
            print(counter)
        except NameError:
            print("** class doesn't exist **")


    def strip_clean(self, args):
        """strips the argument and return a string of command
        Args:
            args: input list of args
        Return:
            returns string of argumetns
        """
        isi_list = []
        isi_list.append(args[0])
        try:
            my_dict = eval(
                args[1][args[1].find('{'):args[1].find('}')+1])
        except Exception:
            my_dict = None
        if isinstance(my_dict, dict):
            new_str = args[1][args[1].find('(')+1:args[1].find(')')]
            isi_list.append(((new_str.split(", "))[0]).strip('"'))
            isi_list.append(my_dict)
            return isi_list
        new_str = args[1][args[1].find('(')+1:args[1].find(')')]
        isi_list.append(" ".join(new_str.split(", ")))
        return " ".join(i for i in isi_list)


    def default(self, line):
        """retrieve all instances of a class and
        retrieve the number of instances
        """
        mc_list = line.split('.')
        if len(mc_list) >= 2:
            if mc_list[1] == "all()":
                self.do_all(mc_list[0])
            elif mc_list[1] == "count()":
                self.count(mc_list[0])
            elif mc_list[1][:4] == "show":
                self.do_show(self.strip_clean(mc_list))
            elif mc_list[1][:7] == "destroy":
                self.do_destroy(self.strip_clean(mc_list))
            elif mc_list[1][:6] == "update":
                args = self.strip_clean(mc_list)
                if isinstance(args, list):
                    obj = storage.all()
                    key = args[0] + ' ' + args[1]
                    for k, v in args[2].items():
                        self.do_update(key + ' "{}" "{}"'.format(k, v))
                else:
                    self.do_update(args)
        else:
            cmd.Cmd.default(self, line)




if __name__ == '__main__':
    HBNBCommand().cmdloop()
