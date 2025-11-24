1、/*  
.common-layout { .el-container {} }： 
这是普通的CSS语法，用于选择具有类名为.common-layout的元素，并在其内部选择具有类名为.el-container的子元素。

.common-layout { & > .el-container {} }： 
这是使用了CSS预处理器（如Sass或Less）的语法。
在这种写法中，&符号表示父选择器（.common-layout），>符号表示-选择-直接子元素。
因此，& > .el-container表示选择.common-layout的直接子元素中具有类名为.el-container的元素。
 */

 2、
// 可以用如下的形式来对数据进行映射处理：比如将后端数据中的0，1，映射为前端的男和女
// 遍历item, map(处理后放回原数据)，map的方式处理后，记得返回item；
list.value = res.data.map((item) => {
item.sexLabel = item.sex === 0 ? "女" : "男";
return item;});


3、v-for循环；
    如果在标签-属性中使用 item的值，使用动态属性的形式： eg: :name="item.name"
    如果在标签-内容中使用 item的值，使用双引号的形式： eg: <p>{{ item.name }}</p>

4、Flask中，request.data属性用于获取请求的原始数据，而request.form属性用于获取解析后的表单数据。如果request.data中有数据，但request.form中没有数据，可能是因为请求的Content-Type不是application/x-www-form-urlencoded或multipart/form-data，导致Flask无法自动解析表单数据。

如果你确定请求的数据是表单数据，可以尝试手动解析数据并将其放置在request.form中。可以使用request.get_data()方法获取原始数据，然后根据请求的Content-Type自行解析数据。
def handle_post_request():
    content_type = request.headers.get('Content-Type')
    
    if content_type == 'application/x-www-form-urlencoded':
        # 解析表单数据
        request.form = request.form.to_dict()
    elif content_type == 'application/json':
        # 解析JSON数据
        request.form = json.loads(request.get_data())
    
    # 现在可以通过request.form获取表单数据
    
    return 'Success'

5、<!-- 通过scope插槽获取待编辑数据 -->
<template #default="scope">
    <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
    <el-button type="primary" size="small">删除</el-button>
</template>

<!-- 6、 return：如果条件为真（即本地存储中不存在'menu'项目），则函数立即返回，不执行后续代码。跟其他语言不一样 -->
<!-- addMenu(state) {
if (!localStorage.getItem('menu')) {
    return
}
const menu = JSON.parse(localStorage.getItem('menu'))
state.menu = menu
} -->