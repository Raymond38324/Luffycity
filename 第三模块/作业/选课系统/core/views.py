# encoding: utf-8
from db.dbs import All_db
from abc import ABCMeta, abstractmethod
from log.log import access_log, student_log, teacher_log, manage_log
from time import sleep

# 　初始化数据库对象
db = All_db()


def checked_input(input_tuple):
    """
    :param input_tuple:<tuple> (<str>,[<str>,<list>,<dict>,<int>]) input的参数和类型
    :return: <tuple[1]> 符合类型的数据
    """
    i, j = input_tuple
    # 元祖解包
    try:
        res = j(input(i).strip())
        # 能得到正确结果，则返回
        return res
    except ValueError:
        # 不能得到正确结果则让用户重新输入
        print("输入有误，亲重新输入：")
        return checked_input(input_tuple)


# 检查密码是否正确的函数
def check_pwd(db_passwd, input_passwd): return db_passwd == input_passwd


class BaseView(object, metaclass=ABCMeta):
    """
    视图类的基类
    """

    def __init__(self, user):
        """
        :param user:<core.user,User＞　各种用户对象
        """
        self.user = user

    @staticmethod
    def add_role(iter_obj, return_list=True):
        """
        :param iter_obj: <dict>{<str>:<obj>} 包含名称和实例的字典
        :return: <list>[<object>]
        """
        choice_dic = {}
        # 初始化字典
        for i, v in enumerate(iter_obj, 1):
            print('{}:{}'.format(i, v))
            choice_dic[str(i)] = v
            # 将转换后的数据存如字典
        if return_list:
            print('输入序号选择数据.可输入多个以，隔开:')
        else:
            print("输入序号选择数据")
        choice = input(">>>")
        try:
            # 　能取到值就返回，不能取到值就说明输入有误，　重新输入
            if return_list:
                return [iter_obj[choice_dic[i]] for i in choice.split(
                    ',')] if ',' in choice else [iter_obj[choice_dic[choice]]]
            else:
                return iter_obj[choice_dic[choice]]
        except KeyError:
            print("输入的选项不存在！")
            return self.add_role(iter_obj)

    @abstractmethod
    def display_menu(self):
        """
        定义一个继承的类必须实现的方法
        """
        pass

    @staticmethod
    def exit_program(user):
        """
        :param user: <core.user.User>用户对象
        """
        access_log.info("%s退出了系统" % user)
        exit()


class TeacherView(BaseView):
    def display_menu(self):
        """
        根据不同的输入选择不同的功能
        """
        while True:
            print("""
            输入序号选择功能
            1. 上课时选择班级
            2. 查看班级学生列表
            3. 更改学生的分数
            4. 退出
            """)
            choice = input(">>>")
            if choice == "1":
                self.choice_class()
            elif choice == "2":
                self.query_students_info()
            elif choice == "3":
                student_out = input("输入学员名称:")
                # 学院存在则取得学员信息并返回，不存在则提示用户
                if student_out in db.all_students:
                    student_out = db.all_students.get(student_out)
                    self.modify_mark(student_out)
                else:
                    print("该学员不存在")
            elif choice == "4":
                # 退出程序
                self.exit_program(self.user)

    def choice_class(self):
        """
        选择班级并打印
        """
        classes = self.add_role(self.user.classes, return_list=False)
        teacher_log.info("{}选择了班级{}".format(self.user, classes))

    def query_students_info(self):
        """
        选择班级并打印学生姓名
        """
        res = self.add_role(self.user.classes, return_list=False)
        teacher_log.info("{}查看了班级{}的学生列表".format(self.user, res))
        print("这个班级的学生有：")
        for student in res.students:
            print(student.name)

    def modify_mark(self, student):
        """
        修改学员成绩
        :param student:<core.user.Student> object
        """
        # 如果学生有mark属性则取得mark属性的值,没有则初始化一个
        if hasattr(student, "mark"):
            res = student.mark
        else:
            """
            生成的字典的格式类似
            {班级一：{课程一：成绩，课程二：成绩}，
            班级二:{课程一:成绩，课程二:成绩}}
            """
            res = {}
            for k, v in student.classes.items():
                res[k] = dict.fromkeys([i.name for i in v.course], 0)

        choice_class = self.add_role(student.classes, return_list=False)

        modify_dict = res.get(choice_class.name)

        for key, value in modify_dict.items():
            print('班级名:{}课程名：{}　成绩：{}'.format(choice_class.name, key, value))
        while True:
            # 修改学员的成绩
            choice = input('输入要更改成绩的课程:')
            if choice in modify_dict:
                score = checked_input(('成绩：', int))
                modify_dict[choice] = score
                teacher_log.info(
                    "{}修改了{} 的 {} 的成绩为{}".format(
                        self.user, student, choice, str(score)))
                break
        res[choice_class.name] = modify_dict
        student.mark = res
        student.save()


class StudentView(BaseView):

    def display_menu(self):
        """
        根据不同的输入选择不同的功能
        """
        while True:
            print("""
            输入序号选择功能：
            1. 交学费:
            2. 选择班级
            3. 退出
            """)
            choice = input(">>>")
            if choice == '2':
                # 调用选择班级函数　
                classes = self.add_role(db.all_class, return_list=False)
                student_log.info("{}选择了班级{}".format(self.user, classes))
                self.user.choose_class(classes)
                print('选择班级成功！')
            elif choice == "1":
                # 如果学院加入了班级　并且没有交学费
                if self.user.classes and not self.user.is_paymented:
                    print("需要交的费用为:", self.user.payment())
                    self.user.is_paymented = True
                    student_log.info("%s交了全部学费" % self.user)
                    self.user.save()
                elif self.user.is_paymented:
                    # 如果学员已经交了学费
                    print("已经交过学费")
                else:
                    print("学员未加入班级！")
            elif choice == "3":
                # 退出程序
                self.exit_program(self.user)
            else:
                print("输入的选项有误，请重新输入!")


class ManageView(BaseView):

    def display_menu(self):
        """
        根据不同的输入选择不同的功能
        """
        while True:
            print(
                """
                1.创建讲师
                2.创建班级
                3.创建课程
                4. 退出
                """)

            choice = input("输入序号选择功能").strip()
            if choice == '1':
                while True:
                    # 生成一个需要的数据列表，之后调用add_teacher生成一个teacher
                    input_list = [
                        checked_input(i) for i in [
                            ('姓名：', str), ('密码：', str), ('年龄：', int), ('性别：', str)]]
                    res = self.add_role(db.all_school, return_list=False)
                    input_list.append(res)
                    self.user.add_teacher(*input_list)
                    break

            elif choice == '2':
                # 输入班级名称　选择老师和课程，并创建老师
                name = input("请输入班级名称：")
                teacher = self.add_role(db.all_teachers)
                course = self.add_role(db.all_course)
                self.user.add_class(name, teacher=teacher, course=course)
                sleep(0.1)
            elif choice == '3':
                # 获取需要的信息，并且创建课程
                input_list = [
                    checked_input(i) for i in [
                        ('名称：', str), ('周期：', str), ('价格：', int)]]
                self.user.add_courses(*input_list)
            elif choice == '4':
                # 退出程序
                self.exit_program(self.user)
            else:
                print('输入的选项有误，请重新输入：')


def get_view(user_name, passwd):
    """
    :param user_name: <str> 用户名
    :param passwd: <str>　密码
    :return: <core.views.BaseView>　view对象
    """
    # 初始化view
    view = None

    # 如果用户存在则获取用户角色对应的view
    if user_name in db.all_admin:
        user = db.all_admin.get(user_name)
        if check_pwd(user.password, passwd):
            view = ManageView(user)
    elif user_name in db.all_teachers:
        user = db.all_teachers.get(user_name)
        if check_pwd(user.password, passwd):
            view = TeacherView(user)
    elif user_name in db.all_students:
        user = db.all_students.get(user_name)
        if check_pwd(user.password, passwd):
            view = StudentView(user)
    else:
        print("用户不存在")
        return
    if not view:
        # 如果view为None则说明，没有获取到view,用户又存在　则原因是密码错误
        print("密码错误")
    access_log.info("%s登陆了系统!" % user)
    return view
